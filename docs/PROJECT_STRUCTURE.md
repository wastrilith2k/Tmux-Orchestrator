# Tmux Orchestrator - Complete Project Structure Documentation

**Date Created**: September 16, 2025
**Version**: 2.0
**Architecture**: Multi-Agent AI Orchestration System with Full Containerization

## 🎯 Project Overview

The Tmux Orchestrator is a sophisticated **autonomous multi-agent AI development system** where Claude agents coordinate development work through both traditional tmux sessions and containerized environments. The system supports persistent work sessions that continue even when disconnected, with agents that can:

- Autonomously develop, test, and deploy applications
- Coordinate with other agents via structured communication
- Self-schedule work and maintain development momentum
- Operate in both host-based (tmux) and containerized (Docker) environments

---

## 📁 Root Directory Structure

### 📋 Core Documentation Files
| File | Purpose | Lines | Description |
|------|---------|-------|-------------|
| `CLAUDE.md` | Agent Behavior Guide | 717 | **Primary agent instructions** - Complete behavioral guidelines for autonomous agents including communication protocols, quality standards, and workflow patterns |
| `README.md` | Project Overview | ~100 | High-level project description, setup instructions, and usage examples |
| `LEARNINGS.md` | Development Insights | ~50 | Key learnings and insights gained during development |

### 🐳 Container Orchestration Files
| File | Purpose | Description |
|------|---------|-------------|
| `docker-compose.containerized.yml` | Complete Containerized Stack | **303 lines** - Full containerized deployment with infrastructure (PostgreSQL, Redis), workspaces, agents, and orchestrator containers |
| `docker-compose.yml` | Standard Composition | Basic docker composition for API and infrastructure services |

---

## 🏗️ Directory Structure Deep Dive

### 🤖 `/agents/` - Agent Implementations
**Purpose**: Contains both traditional shell-based agents and management scripts for autonomous development teams.

| File | Type | Purpose |
|------|------|---------|
| `agent_communication.sh` | Shell Script | Inter-agent communication protocol implementation |
| `claude_agent_manager.py` | Python Module | Central agent lifecycle management and coordination |
| `devops_agent.sh` | Shell Agent | Infrastructure, deployment, and CI/CD operations |
| `project_manager_agent.sh` | Shell Agent | **148 lines** - Quality assurance, team coordination, git management, testing oversight |
| `qa_engineer_agent.sh` | Shell Agent | Testing, validation, and quality control automation |

**Key Features**:
- Each agent follows the behavioral patterns defined in `CLAUDE.md`
- Agents coordinate via tmux messaging and Redis pub/sub
- Self-scheduling for autonomous operation
- Mandatory git commits every 30 minutes

### 📁 `/bin/` - Executable Scripts
**Purpose**: Core operational scripts and utilities for system management.

| File | Purpose | Description |
|------|---------|-------------|
| `send-claude-message.sh` | **Critical Communication** | Universal agent messaging script with 0.5s timing built-in |
| `schedule_with_note.sh` | Self-Scheduling | Enables agents to schedule their own check-ins for autonomous operation |
| `setup_claude_agent.sh` | Agent Initialization | Creates and configures new Claude agents in tmux sessions |
| `start_orchestrator.sh` | System Startup | Main orchestrator startup and session management |
| `deploy-containerized.sh` | Container Deployment | Launches full containerized system stack |
| `validate_architecture.sh` | System Validation | Verifies system integrity and configuration |
| `demo_learning_system.sh` | Demo System | Demonstrates system capabilities and learning features |

**Critical Pattern**: Always use `send-claude-message.sh` instead of raw tmux commands to prevent timing issues.

### 🔧 `/utils/` - Utility Modules
**Purpose**: Core Python modules providing programmatic system control and monitoring.

| File | Lines | Purpose |
|------|-------|---------|
| `tmux_utils.py` | 251 | **Primary tmux interface** - Programmatic tmux session management with safety checks |
| `hub_orchestrator.py` | ~200 | High-level orchestration and agent coordination |
| `approval_monitor.py` | ~150 | Quality gates and approval workflow management |
| `mock_api_server.py` | ~100 | Development and testing API server |

**Key Capabilities**:
- Full tmux session monitoring and control
- Agent status tracking and health checks
- Automated quality assurance workflows
- Development environment simulation

### 🐳 `/containers/` - Container Infrastructure
**Purpose**: Complete containerized implementation of the agent system.

#### `/containers/agent-scripts/`
| File | Lines | Purpose |
|------|-------|---------|
| `containerized-engineer-agent.py` | 217 | **Redis-based engineer agent** - Autonomous development with pub/sub communication |
| `containerized-pm-agent.py` | ~200 | **Project manager in container** - Quality oversight and team coordination |

#### `/containers/orchestrator/`
| File | Purpose |
|------|---------|
| `orchestrator_main.py` | Main containerized orchestrator process |
| `health_check.py` | Container health monitoring and status reporting |

#### Configuration Files
| File | Purpose |
|------|---------|
| `entrypoint.sh` | Agent container initialization and setup |
| `workspace-entrypoint.sh` | Workspace container bootstrap |

**Architecture**: Redis pub/sub replaces direct tmux messaging for container communication.

### 🏢 `/admin-system/` - Administrative Infrastructure
**Purpose**: Complete administrative dashboard and monitoring system.

#### `/admin-system/api-gateway/`
| File | Purpose |
|------|---------|
| `main.py` | FastAPI gateway for system management |
| `config.py` | Configuration management |
| `database.py` | PostgreSQL integration |
| `models.py` | Data models and schemas |
| `requirements.txt` | Python dependencies |

#### `/admin-system/dashboard/` (Next.js)
| Component | Purpose |
|-----------|---------|
| `package.json` | Next.js application configuration |
| `tsconfig.json` | TypeScript configuration |
| `.next/` | Build artifacts and generated files |

#### `/admin-system/monitoring/`
| File | Purpose |
|------|---------|
| `prometheus.yml` | Metrics collection configuration |
| `loki-config.yml` | Log aggregation setup |
| `docker-compose.admin.yml` | Administrative services stack |

### 📚 `/docs/` - Documentation Suite
**Purpose**: Comprehensive project documentation and analysis.

| File | Purpose |
|------|---------|
| `SELF_LEARNING_APPROVALS.md` | Agent learning and approval workflows |
| `TASKS.md` | Task definitions and management |
| `systems-architecture-analysis.md` | Detailed architectural analysis |

#### `/docs/analysis/` - Technical Analysis
| File | Purpose |
|------|---------|
| `setup-test-project.sh` | Test project creation and validation |
| `test-project-analysis.md` | Project analysis methodologies |
| `test-project-gap-analysis.md` | Gap analysis and improvement recommendations |
| `task-completion-checklist.md` | Quality assurance checklists |

### 🧪 `/tests/` - Testing Infrastructure
**Purpose**: Comprehensive system testing and validation.

| File | Purpose |
|------|---------|
| `test_system.py` | **Primary system tests** - End-to-end testing of agent coordination |
| `test_containerized_system.py` | **Container deployment tests** - Validation of containerized architecture |

### 📊 `/logs/` - Logging and Monitoring
**Purpose**: Centralized logging and communication tracking.

| Directory | Purpose |
|-----------|---------|
| `/logs/agents/` | Individual agent activity logs |
| `/logs/communications/` | Inter-agent message tracking |
| `next_check_note.txt` | Scheduling and checkpoint information |

### 🚀 `/deployment/` - Deployment Configuration
**Purpose**: Production deployment scripts and configurations.

Contains deployment manifests, environment configurations, and production setup scripts.

### 🔧 `/api/` - API Services
**Purpose**: RESTful API interface for system interaction.

| File | Purpose |
|------|---------|
| `main.py` | FastAPI application entry point |
| `requirements.txt` | API service dependencies |

### ⚙️ `/config/` - System Configuration
**Purpose**: Environment-specific configurations and settings.

Contains configuration files for different deployment environments and agent behaviors.

### 📝 `/src/` - Source Code Modules
**Purpose**: Core system source code organized by component.

#### `/src/agents/`
Core agent implementation modules.

#### `/src/orchestrator/`
Central orchestration system components.

#### `/src/utils/`
Shared utility modules and helpers.

### 📋 `/tasks/` - Task Management
**Purpose**: Task definitions and workflow management.

| File | Purpose |
|------|---------|
| `integrate-contains-studio-agents.md` | Integration task specifications |

---

## 🔗 System Architecture Patterns

### Communication Flow
```
Orchestrator (Coordination)
    ↕️ (tmux/Redis messaging)
Project Manager (Quality)
    ↕️ (structured protocols)
Engineers/Specialists (Implementation)
```

### Deployment Options

#### 1. **Host-Based Deployment**
- Uses traditional tmux sessions
- Direct shell script communication via `send-claude-message.sh`
- Persistent sessions survive disconnection
- Full shell environment access

#### 2. **Containerized Deployment**
- Docker containers for each agent
- Redis pub/sub communication
- Isolated execution environments
- Scalable infrastructure with PostgreSQL and Redis

### Critical Workflow Patterns

#### Agent Communication Protocol
```bash
# ALWAYS use the dedicated script - never manual tmux commands
./bin/send-claude-message.sh session:window "message content"
```

#### Self-Scheduling Pattern
```bash
# Agents schedule their own check-ins
./bin/schedule_with_note.sh 30 "Continue feature implementation" "session:window"
```

#### Git Safety Rules (CRITICAL)
```bash
# Every agent must commit every 30 minutes
git add -A
git commit -m "Progress: specific description of work done"
```

---

## 🎯 Key System Features

### ✅ **Autonomous Operation**
- Agents work independently with minimal oversight
- Self-scheduling maintains development momentum
- Persistent sessions continue work across disconnections

### ✅ **Quality Assurance**
- Project Managers enforce coding standards
- Mandatory testing before feature approval
- Regular git commits prevent work loss

### ✅ **Scalable Architecture**
- Both host-based and containerized deployment options
- Redis pub/sub enables distributed agent communication
- Modular design supports easy extension

### ✅ **Comprehensive Monitoring**
- Full tmux session status tracking
- Agent health monitoring and logging
- Administrative dashboard for system oversight

---

## 🚀 Quick Start Guide

### Host-Based Deployment
```bash
./bin/start_orchestrator.sh
./bin/setup_claude_agent.sh project-name /path/to/project
```

### Containerized Deployment
```bash
./bin/deploy-containerized.sh
docker-compose -f docker-compose.containerized.yml up
```

### System Validation
```bash
./bin/validate_architecture.sh
python tests/test_system.py
```

---

## 📖 Essential Reading

1. **`CLAUDE.md`** (717 lines) - **MUST READ** - Complete agent behavioral guidelines
2. **`docker-compose.containerized.yml`** - Full containerized architecture
3. **`utils/tmux_utils.py`** - Programmatic system control interface
4. **`agents/project_manager_agent.sh`** - Quality assurance patterns

---

**Last Updated**: September 16, 2025
**System Status**: ✅ Fully Containerized & Organized
**Total Files Documented**: 80+ files across 25+ directories

This documentation provides a complete understanding of the Tmux Orchestrator's architecture, enabling autonomous AI agents to coordinate sophisticated development workflows through both traditional and containerized environments.