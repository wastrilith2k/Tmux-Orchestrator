from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio
import os
import sys
from datetime import datetime
from typing import List, Optional, Dict, Any
import structlog
import redis.asyncio as redis
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

# Add the current directory to the Python path
sys.path.append('/app')

from database import Database
from models import (
    Project, ProjectCreate, ProjectUpdate, ProjectStatus,
    Agent, AgentCreate, Message, MessageCreate,
    HealthCheck, SystemMetrics
)
from config import Settings

# Initialize structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Initialize settings
settings = Settings()

# Initialize FastAPI app
app = FastAPI(
    title="Tmux Orchestrator Hub API",
    description="Central API for managing distributed tmux orchestrator projects",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')
ACTIVE_PROJECTS = Gauge('active_projects_total', 'Number of active projects')
ACTIVE_AGENTS = Gauge('active_agents_total', 'Number of active agents')

# Global variables
db: Database = None
redis_client: redis.Redis = None

@app.on_event("startup")
async def startup_event():
    """Initialize database and Redis connections on startup"""
    global db, redis_client

    logger.info("Starting up Hub API Gateway...")

    # Initialize database
    try:
        db = Database(settings.database_url)
        await db.connect()
        logger.info("Database connection established")
    except Exception as e:
        logger.error("Failed to connect to database", error=str(e))
        raise

    # Initialize Redis
    try:
        redis_client = redis.from_url(settings.redis_url)
        await redis_client.ping()
        logger.info("Redis connection established")
    except Exception as e:
        logger.error("Failed to connect to Redis", error=str(e))
        raise

    logger.info("Hub API Gateway startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up connections on shutdown"""
    global db, redis_client

    logger.info("Shutting down Hub API Gateway...")

    if db:
        await db.disconnect()
        logger.info("Database connection closed")

    if redis_client:
        await redis_client.close()
        logger.info("Redis connection closed")

# Dependency injection
async def get_database() -> Database:
    """Get database connection"""
    if not db:
        raise HTTPException(status_code=500, detail="Database not initialized")
    return db

async def get_redis() -> redis.Redis:
    """Get Redis connection"""
    if not redis_client:
        raise HTTPException(status_code=500, detail="Redis not initialized")
    return redis_client

# Health check endpoint
@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint for load balancers and monitoring"""
    try:
        # Check database
        db_healthy = await db.health_check() if db else False

        # Check Redis
        redis_healthy = False
        if redis_client:
            try:
                await redis_client.ping()
                redis_healthy = True
            except:
                pass

        status = "healthy" if db_healthy and redis_healthy else "unhealthy"

        return HealthCheck(
            status=status,
            timestamp=datetime.utcnow(),
            database=db_healthy,
            redis=redis_healthy,
            version="1.0.0"
        )
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        return HealthCheck(
            status="unhealthy",
            timestamp=datetime.utcnow(),
            database=False,
            redis=False,
            version="1.0.0"
        )

# Metrics endpoint for Prometheus
@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# Project management endpoints
@app.post("/api/projects", response_model=Project, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    db: Database = Depends(get_database),
    redis: redis.Redis = Depends(get_redis)
):
    """Create a new project orchestrator"""
    try:
        logger.info("Creating new project", project_name=project_data.name)

        # Create project in database
        project = await db.create_project(project_data)

        # Publish event to Redis for project orchestrator creation
        await redis.publish(
            "project.create",
            project.json()
        )

        REQUEST_COUNT.labels(method="POST", endpoint="/api/projects", status="201").inc()
        ACTIVE_PROJECTS.inc()

        logger.info("Project created successfully", project_id=project.project_id)
        return project

    except Exception as e:
        logger.error("Failed to create project", error=str(e))
        REQUEST_COUNT.labels(method="POST", endpoint="/api/projects", status="500").inc()
        raise HTTPException(status_code=500, detail=f"Failed to create project: {str(e)}")

@app.get("/api/projects", response_model=List[Project])
async def list_projects(
    status_filter: Optional[str] = None,
    db: Database = Depends(get_database)
):
    """List all projects with optional status filter"""
    try:
        projects = await db.list_projects(status_filter)
        REQUEST_COUNT.labels(method="GET", endpoint="/api/projects", status="200").inc()
        return projects
    except Exception as e:
        logger.error("Failed to list projects", error=str(e))
        REQUEST_COUNT.labels(method="GET", endpoint="/api/projects", status="500").inc()
        raise HTTPException(status_code=500, detail=f"Failed to list projects: {str(e)}")

@app.get("/api/projects/{project_id}", response_model=Project)
async def get_project(
    project_id: str,
    db: Database = Depends(get_database)
):
    """Get specific project details"""
    try:
        project = await db.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        REQUEST_COUNT.labels(method="GET", endpoint="/api/projects/{id}", status="200").inc()
        return project
    except HTTPException:
        REQUEST_COUNT.labels(method="GET", endpoint="/api/projects/{id}", status="404").inc()
        raise
    except Exception as e:
        logger.error("Failed to get project", project_id=project_id, error=str(e))
        REQUEST_COUNT.labels(method="GET", endpoint="/api/projects/{id}", status="500").inc()
        raise HTTPException(status_code=500, detail=f"Failed to get project: {str(e)}")

@app.put("/api/projects/{project_id}", response_model=Project)
async def update_project(
    project_id: str,
    project_update: ProjectUpdate,
    db: Database = Depends(get_database),
    redis: redis.Redis = Depends(get_redis)
):
    """Update project configuration"""
    try:
        project = await db.update_project(project_id, project_update)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # Publish update event
        await redis.publish(
            f"project.{project_id}.update",
            project.json()
        )

        REQUEST_COUNT.labels(method="PUT", endpoint="/api/projects/{id}", status="200").inc()
        return project
    except HTTPException:
        REQUEST_COUNT.labels(method="PUT", endpoint="/api/projects/{id}", status="404").inc()
        raise
    except Exception as e:
        logger.error("Failed to update project", project_id=project_id, error=str(e))
        REQUEST_COUNT.labels(method="PUT", endpoint="/api/projects/{id}", status="500").inc()
        raise HTTPException(status_code=500, detail=f"Failed to update project: {str(e)}")

@app.delete("/api/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    db: Database = Depends(get_database),
    redis: redis.Redis = Depends(get_redis)
):
    """Delete a project and stop its orchestrator"""
    try:
        success = await db.delete_project(project_id)
        if not success:
            raise HTTPException(status_code=404, detail="Project not found")

        # Publish delete event
        await redis.publish(
            f"project.{project_id}.delete",
            '{"action": "delete"}'
        )

        REQUEST_COUNT.labels(method="DELETE", endpoint="/api/projects/{id}", status="204").inc()
        ACTIVE_PROJECTS.dec()

    except HTTPException:
        REQUEST_COUNT.labels(method="DELETE", endpoint="/api/projects/{id}", status="404").inc()
        raise
    except Exception as e:
        logger.error("Failed to delete project", project_id=project_id, error=str(e))
        REQUEST_COUNT.labels(method="DELETE", endpoint="/api/projects/{id}", status="500").inc()
        raise HTTPException(status_code=500, detail=f"Failed to delete project: {str(e)}")

# Agent management endpoints
@app.get("/api/projects/{project_id}/agents", response_model=List[Agent])
async def list_project_agents(
    project_id: str,
    db: Database = Depends(get_database)
):
    """List all agents for a specific project"""
    try:
        agents = await db.list_project_agents(project_id)
        REQUEST_COUNT.labels(method="GET", endpoint="/api/projects/{id}/agents", status="200").inc()
        return agents
    except Exception as e:
        logger.error("Failed to list project agents", project_id=project_id, error=str(e))
        REQUEST_COUNT.labels(method="GET", endpoint="/api/projects/{id}/agents", status="500").inc()
        raise HTTPException(status_code=500, detail=f"Failed to list agents: {str(e)}")

# Message handling endpoints
@app.post("/api/projects/{project_id}/message", status_code=status.HTTP_202_ACCEPTED)
async def send_message_to_project(
    project_id: str,
    message: MessageCreate,
    db: Database = Depends(get_database),
    redis: redis.Redis = Depends(get_redis)
):
    """Send message to a project's agents"""
    try:
        # Store message in database
        message_record = await db.create_message(project_id, message)

        # Publish to Redis for real-time delivery
        await redis.publish(
            f"project.{project_id}.messages",
            message_record.json()
        )

        REQUEST_COUNT.labels(method="POST", endpoint="/api/projects/{id}/message", status="202").inc()
        return {"message": "Message queued for delivery", "message_id": message_record.message_id}

    except Exception as e:
        logger.error("Failed to send message", project_id=project_id, error=str(e))
        REQUEST_COUNT.labels(method="POST", endpoint="/api/projects/{id}/message", status="500").inc()
        raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")

# System status endpoints
@app.get("/api/system/status", response_model=SystemMetrics)
async def get_system_status(db: Database = Depends(get_database)):
    """Get overall system status and metrics"""
    try:
        metrics = await db.get_system_metrics()
        REQUEST_COUNT.labels(method="GET", endpoint="/api/system/status", status="200").inc()
        return metrics
    except Exception as e:
        logger.error("Failed to get system status", error=str(e))
        REQUEST_COUNT.labels(method="GET", endpoint="/api/system/status", status="500").inc()
        raise HTTPException(status_code=500, detail=f"Failed to get system status: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)