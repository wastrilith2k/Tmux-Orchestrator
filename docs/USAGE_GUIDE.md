# Tmux Orchestrator Usage Guide

## Overview
Tmux Orchestrator is a multi-agent autonomous development system supporting both host-based (tmux) and containerized (Docker) environments. Agents coordinate via tmux sessions or Redis pub/sub, and all agent state, logs, and coordination files are stored centrally in the `.claude/` directory at the project root.

## Centralized Agent State
- All agent logs, coordination notes, and session metadata are stored in `.claude/`.
- Subdirectories (e.g., `.claude/commands/`) are used for specific agent roles or coordination tasks.
- This keeps the workspace clean and makes it easy to manage or clean up agent files.

## Cleaning Up Unneeded Files
- To remove old or unneeded agent state files, simply delete contents of `.claude/` except for active coordination files (e.g., `commands/pm-oversight.md`).
- You can automate this with:
  ```bash
  rm -rf .claude/*
  mkdir -p .claude/commands
  # Restore any needed templates or coordination files
  ```

## Dashboard and GUI Interface

Tmux Orchestrator includes a comprehensive web-based dashboard built with Next.js that provides a graphical interface for managing agents, monitoring projects, and viewing system metrics.

### Starting the Dashboard
1. **Launch the admin system:**
   ```bash
   cd admin-system
   docker-compose -f docker-compose.admin.yml up -d
   ```

2. **Access the dashboard:**
   - Open your browser to `http://localhost:3000`
   - The API gateway runs on `http://localhost:8080`

### Dashboard Features

#### Project Management
- **Project Overview**: View all active projects with status indicators
- **Project Details**: Drill down into individual projects to see:
  - Agent assignments and status
  - Git commit history and progress
  - Real-time logs and outputs
  - Performance metrics

#### Agent Monitoring
- **Agent Dashboard**: Real-time view of all active agents
- **Status Indicators**:
  - 🟢 Active and working
  - 🟡 Idle or waiting
  - 🔴 Error or disconnected
- **Communication Logs**: View inter-agent messages and coordination
- **Performance Metrics**: CPU, memory, and task completion rates

#### System Health
- **Infrastructure Monitoring**:
  - Tmux session status
  - Container health (for containerized deployments)
  - Redis pub/sub metrics
  - Database connection status
- **Resource Usage**: Real-time system resource monitoring
- **Alert Management**: Configure notifications for critical issues

#### Task and Workflow Management
- **Spec-Driven Development**:
  - Create and manage feature specifications through the GUI
  - Generate implementation plans and task breakdowns
  - Track progress through the development lifecycle
- **Task Queues**: View and manage pending, in-progress, and completed tasks
- **Quality Gates**: Monitor testing, code review, and deployment stages

### Working Through the GUI

#### Creating a New Project
1. Navigate to the "Projects" section
2. Click "New Project"
3. Fill in project details:
   - Project name and description
   - Repository URL (if applicable)
   - Technology stack preferences
   - Agent team composition (Engineers, QA, DevOps, etc.)
4. Configure deployment preferences (host-based vs containerized)
5. Launch the project - agents will be automatically assigned and initialized

#### Managing Agent Teams
1. Go to "Agent Management"
2. View current agent assignments and workloads
3. Add or remove agents from projects
4. Configure agent-specific parameters:
   - Communication preferences (tmux vs Redis)
   - Quality thresholds
   - Commit frequency settings
5. Monitor agent health and performance metrics

#### Monitoring Project Progress
1. Select a project from the dashboard
2. View real-time progress indicators:
   - Current tasks and completion status
   - Git activity and commit frequency
   - Quality metrics (test coverage, code review status)
   - Agent coordination and communication logs
3. Access detailed logs and debugging information
4. Intervene manually if needed (pause agents, adjust parameters)

#### Using Spec-Driven Development
1. Navigate to "Specifications"
2. Create new feature specifications using the integrated editor
3. Use the `/specify`, `/plan`, `/tasks` workflow through the GUI:
   - Enter feature descriptions in natural language
   - Review generated specifications and requirements
   - Approve implementation plans
   - Monitor task execution in real-time
4. Track feature development from conception to deployment

## Running Multiple Projects at Once
Tmux Orchestrator is designed to support multiple concurrent projects through both command-line and GUI interfaces.

### Command-Line Approach
1. **Create a new tmux session for each project:**
   ```bash
   tmux new-session -d -s <project-name> -c /path/to/project
   ```
2. **Set up standard windows for each session:**
   - Claude-Agent
   - Shell
   - Dev-Server
3. **Brief the agent with project-specific responsibilities and constraints.**
4. **Agents will use `.claude/` for all coordination and state files.**
5. **Monitor and manage sessions using the orchestrator tools and scripts.**

### GUI Approach
1. **Access the dashboard** at `http://localhost:3000`
2. **Create multiple projects** through the "New Project" interface
3. **Configure agent teams** for each project independently
4. **Monitor all projects** from the unified dashboard view
5. **Switch between projects** using the project selector

### Example: Launching Two Projects
```bash
# Project Alpha (Command Line)
cd ~/Coding/AlphaProject
./bin/start_orchestrator.sh

# Project Beta (GUI)
# 1. Open dashboard at localhost:3000
# 2. Click "New Project"
# 3. Configure BetaProject settings
# 4. Launch agents through GUI
```

Each project maintains its own `.claude/` directory for agent state and coordination, visible through both command-line tools and the dashboard interface.

### Dashboard Architecture and Technology Stack

The Tmux Orchestrator dashboard is built with modern web technologies for performance and real-time capabilities:

#### Frontend (Next.js Dashboard)
- **Framework**: Next.js 14 with React and TypeScript
- **Styling**: Tailwind CSS for responsive design
- **Real-time Updates**: WebSocket connections for live agent monitoring
- **State Management**: React Query for server state and caching
- **UI Components**: Custom component library with dark/light theme support
- **Charts and Metrics**: Interactive visualizations for system monitoring

#### Backend (FastAPI API Gateway)
- **Framework**: FastAPI with async/await support
- **Features**:
  - Project and agent management endpoints
  - Real-time WebSocket connections
  - Health checks and system monitoring
  - Authentication and authorization
  - Metrics collection and aggregation
- **Integration**: Direct connection to tmux sessions and Redis pub/sub

#### Database and Storage
- **Primary Database**: PostgreSQL for persistent project and agent data
- **Cache Layer**: Redis for real-time messaging and session state
- **Message Queue**: Redis pub/sub for inter-agent communication
- **File Storage**: Local filesystem integration for project files and logs

#### Monitoring and Observability
- **Metrics**: Custom metrics dashboard with system resource monitoring
- **Logging**: Centralized logging with search and filtering capabilities
- **Health Checks**: Automated monitoring of all system components
- **Alerts**: Configurable notifications for critical system events

### API Endpoints
The dashboard exposes a comprehensive REST API for programmatic access:

```bash
# Project Management
GET /api/projects              # List all projects
POST /api/projects             # Create new project
GET /api/projects/{id}         # Get project details
PUT /api/projects/{id}         # Update project
DELETE /api/projects/{id}      # Delete project

# Agent Management
GET /api/agents                # List all agents
GET /api/agents/{id}/status    # Get agent status
POST /api/agents/{id}/message  # Send message to agent
GET /api/agents/{id}/logs      # Get agent logs

# System Health
GET /api/health                # Overall system health
GET /api/metrics               # System metrics
GET /api/sessions              # Tmux session status
```

### Customization and Configuration
The dashboard supports extensive customization through configuration files:

```json
{
  "dashboard": {
    "theme": "dark|light|auto",
    "refreshInterval": 5000,
    "maxLogLines": 1000,
    "alertThresholds": {
      "cpu": 80,
      "memory": 85,
      "diskSpace": 90
    }
  },
  "agents": {
    "defaultCommitInterval": 30,
    "maxIdleTime": 300,
    "communicationProtocol": "redis|tmux"
  }
}
```

## Best Practices
- **Centralize agent files:** Always use `.claude/` for agent state and coordination.
- **Clean up regularly:** Remove old files from `.claude/` to keep the workspace tidy.
- **Use tmux sessions:** Each project should have its own tmux session for isolation.
- **Monitor agent logs:** Check `.claude/` and `logs/` for agent activity and troubleshooting.
- **Leverage containerization:** For scalable deployments, use `docker-compose.containerized.yml`.

## Troubleshooting
- If agents are not coordinating, check `.claude/commands/` for missing or corrupted files.
- If sessions are not persistent, verify tmux and Docker configurations.
- For advanced orchestration, refer to `CLAUDE.md` and the Spec Kit integration documentation.

---

**For more details, see:**
- `CLAUDE.md` (agent behavior and orchestration)
- `docs/PROJECT_STRUCTURE.md` (project architecture)
- `docs/SPEC_KIT_DEMO.md` (spec-driven development workflow)
