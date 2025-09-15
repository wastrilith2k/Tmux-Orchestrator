import asyncpg
import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import structlog
from models import (
    Project, ProjectCreate, ProjectUpdate, ProjectStatus,
    Agent, AgentCreate, AgentStatus,
    Message, MessageCreate, MessageType,
    SystemMetrics, ResourceAllocation, Event
)

logger = structlog.get_logger()

class Database:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        """Initialize database connection pool"""
        try:
            self.pool = await asyncpg.create_pool(
                self.database_url,
                min_size=2,
                max_size=10,
                command_timeout=60
            )
            logger.info("Database connection pool created")
        except Exception as e:
            logger.error("Failed to create database pool", error=str(e))
            raise

    async def disconnect(self):
        """Close database connection pool"""
        if self.pool:
            await self.pool.close()
            logger.info("Database connection pool closed")

    async def health_check(self) -> bool:
        """Check database health"""
        try:
            if not self.pool:
                return False
            async with self.pool.acquire() as connection:
                await connection.fetchval("SELECT 1")
            return True
        except Exception:
            return False

    # Project management methods
    async def create_project(self, project_data: ProjectCreate) -> Project:
        """Create a new project in the database"""
        project_id = f"{project_data.name.lower().replace(' ', '-')}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        async with self.pool.acquire() as connection:
            try:
                row = await connection.fetchrow("""
                    INSERT INTO projects (
                        project_id, name, description, project_type, project_path,
                        cpu_limit, memory_limit, storage_limit, auto_start, auto_scale,
                        tags, metadata, status
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
                    RETURNING *
                """,
                    project_id, project_data.name, project_data.description,
                    project_data.project_type, project_data.project_path,
                    project_data.cpu_limit, project_data.memory_limit, project_data.storage_limit,
                    project_data.auto_start, project_data.auto_scale,
                    json.dumps(project_data.tags), json.dumps(project_data.metadata),
                    ProjectStatus.PENDING
                )

                # Log event
                await self._log_event(connection, "project_created", "project", {
                    "project_id": project_id,
                    "name": project_data.name,
                    "type": project_data.project_type
                })

                return self._row_to_project(row)
            except Exception as e:
                logger.error("Failed to create project", error=str(e))
                raise

    async def list_projects(self, status_filter: Optional[str] = None) -> List[Project]:
        """List all projects with optional status filter"""
        async with self.pool.acquire() as connection:
            if status_filter:
                rows = await connection.fetch(
                    "SELECT * FROM projects WHERE status = $1 ORDER BY created_at DESC",
                    status_filter
                )
            else:
                rows = await connection.fetch(
                    "SELECT * FROM projects ORDER BY created_at DESC"
                )

            return [self._row_to_project(row) for row in rows]

    async def get_project(self, project_id: str) -> Optional[Project]:
        """Get a specific project by ID (UUID)"""
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(
                "SELECT * FROM projects WHERE id = $1",
                project_id
            )
            return self._row_to_project(row) if row else None

    async def update_project(self, project_id: str, project_update: ProjectUpdate) -> Optional[Project]:
        """Update a project"""
        update_fields = []
        values = []
        value_idx = 1

        for field, value in project_update.dict(exclude_unset=True).items():
            if field in ["tags", "metadata"]:
                update_fields.append(f"{field} = ${value_idx}")
                values.append(json.dumps(value))
            else:
                update_fields.append(f"{field} = ${value_idx}")
                values.append(value)
            value_idx += 1

        if not update_fields:
            return await self.get_project(project_id)

        values.append(project_id)
        query = f"""
            UPDATE projects
            SET {', '.join(update_fields)}, updated_at = NOW()
            WHERE id = ${value_idx}
            RETURNING *
        """

        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(query, *values)
            if row:
                await self._log_event(connection, "project_updated", "project", {
                    "project_id": project_id,
                    "updated_fields": list(project_update.dict(exclude_unset=True).keys())
                })
            return self._row_to_project(row) if row else None

    async def delete_project(self, project_id: str) -> bool:
        """Delete a project"""
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                # Check if project exists
                exists = await connection.fetchval(
                    "SELECT 1 FROM projects WHERE id = $1",
                    project_id
                )
                if not exists:
                    return False

                # Delete project (cascades to related tables)
                await connection.execute(
                    "DELETE FROM projects WHERE id = $1",
                    project_id
                )

                await self._log_event(connection, "project_deleted", "project", {
                    "project_id": project_id
                })

                return True

    async def update_project_heartbeat(self, project_id: str) -> bool:
        """Update project heartbeat timestamp"""
        async with self.pool.acquire() as connection:
            result = await connection.execute(
                "UPDATE projects SET last_heartbeat = NOW() WHERE project_id = $1",
                project_id
            )
            return result == "UPDATE 1"

    # Agent management methods
    async def create_agent(self, agent_data: AgentCreate) -> Agent:
        """Create a new agent"""
        async with self.pool.acquire() as connection:
            # Get project internal ID
            project_internal_id = await connection.fetchval(
                "SELECT id FROM projects WHERE project_id = $1",
                agent_data.project_id
            )
            if not project_internal_id:
                raise ValueError(f"Project {agent_data.project_id} not found")

            row = await connection.fetchrow("""
                INSERT INTO agents (
                    project_id, agent_type, agent_role, agent_name,
                    tmux_session, tmux_window, status
                ) VALUES ($1, $2, $3, $4, $5, $6, $7)
                RETURNING *
            """,
                project_internal_id, agent_data.agent_type, agent_data.agent_role,
                agent_data.agent_name, agent_data.tmux_session, agent_data.tmux_window,
                AgentStatus.INACTIVE
            )

            await self._log_event(connection, "agent_created", "agent", {
                "project_id": agent_data.project_id,
                "agent_type": agent_data.agent_type,
                "agent_role": agent_data.agent_role
            })

            return self._row_to_agent(row)

    async def list_project_agents(self, project_id: str) -> List[Agent]:
        """List all agents for a project"""
        async with self.pool.acquire() as connection:
            rows = await connection.fetch("""
                SELECT a.* FROM agents a
                JOIN projects p ON a.project_id = p.id
                WHERE p.project_id = $1
                ORDER BY a.created_at ASC
            """, project_id)

            return [self._row_to_agent(row) for row in rows]

    async def update_agent_status(self, agent_id: str, status: AgentStatus) -> bool:
        """Update agent status"""
        async with self.pool.acquire() as connection:
            result = await connection.execute(
                "UPDATE agents SET status = $1, last_activity = NOW() WHERE id = $2",
                status, agent_id
            )
            return result == "UPDATE 1"

    # Message handling methods
    async def create_message(self, project_id: str, message_data: MessageCreate) -> Message:
        """Create a new message"""
        message_id = f"msg_{uuid.uuid4().hex[:12]}"

        async with self.pool.acquire() as connection:
            # Get project internal ID
            project_internal_id = await connection.fetchval(
                "SELECT id FROM projects WHERE project_id = $1",
                project_id
            )
            if not project_internal_id:
                raise ValueError(f"Project {project_id} not found")

            # Calculate expiry time if timeout is set
            expires_at = None
            if message_data.response_timeout:
                expires_at = datetime.utcnow() + timedelta(seconds=message_data.response_timeout)

            row = await connection.fetchrow("""
                INSERT INTO messages (
                    message_id, sender_type, sender_id, recipient_type, recipient_id,
                    project_id, message_type, content, metadata, priority,
                    requires_response, response_timeout, expires_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
                RETURNING *
            """,
                message_id, "hub", None, "agent", message_data.recipient_id,
                project_internal_id, message_data.message_type, message_data.content,
                json.dumps(message_data.metadata), message_data.priority,
                message_data.requires_response, message_data.response_timeout, expires_at
            )

            return self._row_to_message(row)

    # System metrics methods
    async def get_system_metrics(self) -> SystemMetrics:
        """Get system-wide metrics"""
        async with self.pool.acquire() as connection:
            # Get project counts
            total_projects = await connection.fetchval("SELECT COUNT(*) FROM projects")
            active_projects = await connection.fetchval(
                "SELECT COUNT(*) FROM projects WHERE status IN ('running', 'active')"
            )

            # Get agent counts
            total_agents = await connection.fetchval("SELECT COUNT(*) FROM agents")
            active_agents = await connection.fetchval(
                "SELECT COUNT(*) FROM agents WHERE status = 'active'"
            )

            # Get message count for today
            today = datetime.utcnow().date()
            total_messages_today = await connection.fetchval(
                "SELECT COUNT(*) FROM messages WHERE DATE(created_at) = $1",
                today
            )

            return SystemMetrics(
                total_projects=total_projects or 0,
                active_projects=active_projects or 0,
                total_agents=total_agents or 0,
                active_agents=active_agents or 0,
                total_messages_today=total_messages_today or 0,
                system_cpu_usage=0.0,  # TODO: Implement system monitoring
                system_memory_usage=0.0,  # TODO: Implement system monitoring
                uptime_seconds=0  # TODO: Implement uptime tracking
            )

    # Utility methods
    def _row_to_project(self, row) -> Project:
        """Convert database row to Project model"""
        return Project(
            id=str(row['id']),
            project_id=row['project_id'],
            name=row['name'],
            description=row['description'],
            project_type=row['project_type'],
            project_path=row['project_path'],
            status=row['status'],
            created_at=row['created_at'],
            updated_at=row['updated_at'],
            last_heartbeat=row['last_heartbeat'],
            cpu_limit=float(row['cpu_limit']),
            memory_limit=row['memory_limit'],
            storage_limit=row['storage_limit'],
            auto_start=row['auto_start'],
            auto_scale=row['auto_scale'],
            config_version=row['config_version'],
            internal_ip=row['internal_ip'],
            api_port=row['api_port'],
            tmux_port=row['tmux_port'],
            tags=json.loads(row['tags']) if row['tags'] else {},
            metadata=json.loads(row['metadata']) if row['metadata'] else {}
        )

    def _row_to_agent(self, row) -> Agent:
        """Convert database row to Agent model"""
        return Agent(
            id=str(row['id']),
            project_id=str(row['project_id']),
            agent_type=row['agent_type'],
            agent_role=row['agent_role'],
            agent_name=row['agent_name'],
            status=row['status'],
            tmux_session=row['tmux_session'],
            tmux_window=row['tmux_window'],
            tasks_completed=row['tasks_completed'],
            tasks_failed=row['tasks_failed'],
            average_response_time=row['average_response_time'],
            last_activity=row['last_activity'],
            cpu_usage_percent=float(row['cpu_usage_percent']),
            memory_usage_mb=row['memory_usage_mb'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )

    def _row_to_message(self, row) -> Message:
        """Convert database row to Message model"""
        return Message(
            id=str(row['id']),
            message_id=row['message_id'],
            sender_type=row['sender_type'],
            sender_id=str(row['sender_id']) if row['sender_id'] else None,
            recipient_type=row['recipient_type'],
            recipient_id=str(row['recipient_id']) if row['recipient_id'] else None,
            project_id=str(row['project_id']),
            message_type=row['message_type'],
            content=row['content'],
            metadata=json.loads(row['metadata']) if row['metadata'] else {},
            priority=row['priority'],
            requires_response=row['requires_response'],
            response_timeout=row['response_timeout'],
            status=row['status'],
            delivered_at=row['delivered_at'],
            expires_at=row['expires_at'],
            created_at=row['created_at']
        )

    async def _log_event(self, connection, event_type: str, category: str, data: Dict[str, Any]):
        """Log an event to the events table"""
        await connection.execute("""
            INSERT INTO events (event_type, event_category, event_data)
            VALUES ($1, $2, $3)
        """, event_type, category, json.dumps(data))