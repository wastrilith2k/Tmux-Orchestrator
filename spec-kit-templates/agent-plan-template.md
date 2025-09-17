# Agent Implementation Plan Template
# Adapted from GitHub Spec Kit for Autonomous Agent Development

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Agent**: [AGENT_NAME] | **Input**: Agent specification + Technical details

## Execution Flow (agent_plan command scope)
```
1. Read agent specification requirements
2. Apply technical constraints and agent architecture patterns
3. Generate agent project structure (tmux + containerized versions)
4. Create Phase 0: Agent Research (tools, frameworks, patterns)
5. Create Phase 1: Agent Design & Communication Contracts
6. Create Phase 2: Agent Testing Strategy
7. Document task planning approach for agent_tasks command
8. Return: SUCCESS (ready for agent task generation)
```

## Summary

This implementation plan translates the agent specification into a concrete technical approach for autonomous operation within the Tmux Orchestrator ecosystem.

**Agent Type**: [Engineer/ProjectManager/QA/DevOps/Specialist]
**Operation Mode**: [Host-based tmux / Containerized / Hybrid]
**Communication**: [send-claude-message.sh / Redis pub/sub / Both]

## Agent Architecture Context

### Agent Technology Stack
**Host-Based Implementation**:
- Shell scripts (.sh) for traditional tmux operation
- Direct tmux messaging via send-claude-message.sh
- Native host environment access

**Containerized Implementation**:
- Python scripts (.py) for containerized operation
- Redis pub/sub communication
- Isolated container environments

### Agent Communication Patterns
**Messaging Protocols**:
- Tmux-based: `./send-claude-message.sh session:window "message"`
- Redis-based: `redis.publish("agent:channel", json_message)`
- File-based: Shared workspace file communication

**Coordination Requirements**:
- Status reporting every 30 minutes
- Git commits every 30 minutes
- Health check responses
- Error escalation procedures

## Constitutional Compliance

### Tmux Orchestrator Agent Articles
**Article I: Autonomous Operation Principle**
```text
Every agent MUST operate autonomously without human intervention.
Agents may request clarification but must continue operation
with reasonable defaults while awaiting responses.
```

**Article II: Communication Protocol Mandate**
```text
All agents MUST use established communication protocols:
- send-claude-message.sh for tmux-based agents
- Redis pub/sub for containerized agents
- Standard message formats for inter-agent coordination
```

**Article III: Quality Assurance Imperative**
```text
All agents MUST implement:
- Self-monitoring and health checks
- Error recovery procedures
- Operation logging for audit trails
- Regular status reporting
```

## Project Structure

### Agent Documentation (this feature)
```
specs/[###-agent-feature]/
├── plan.md              # This file (agent_plan command output)
├── research.md          # Agent tools and frameworks research
├── communication.md     # Inter-agent communication contracts
├── monitoring.md        # Health checks and status reporting
├── recovery.md          # Error handling and recovery procedures
└── tasks.md             # Agent task breakdown (agent_tasks command)
```

### Agent Implementation Structure
```
agents/[agent-name]/
├── host-based/
│   ├── [agent-name].sh           # Main agent script
│   ├── communication.sh          # Messaging functions
│   └── monitoring.sh             # Health check functions
├── containerized/
│   ├── [agent-name].py           # Main agent class
│   ├── communication.py          # Redis pub/sub
│   └── monitoring.py             # Container health checks
└── shared/
    ├── config.json               # Agent configuration
    └── templates/                # Message templates
```

## Phase 0: Agent Research & Setup

### Agent Framework Research
- Evaluate existing agent patterns in /agents/ directory
- Research appropriate libraries for agent functionality
- Identify integration points with tmux_utils.py
- Study CLAUDE.md behavioral guidelines

### Communication Protocol Research
- Map existing tmux messaging patterns
- Analyze Redis pub/sub implementation
- Design message schemas for agent coordination
- Plan backward compatibility between host/container modes

## Phase 1: Agent Design & Contracts

### Communication Contract Design
```yaml
# Agent Message Schema
agent_message:
  from: "agent:type:name"
  to: "agent:type:name" | "broadcast" | "orchestrator"
  type: "status" | "request" | "response" | "alert"
  content:
    message: "Human readable message"
    data: {} # Structured data
    timestamp: "ISO-8601"
    correlation_id: "UUID"
```

### Agent State Management
- Define agent lifecycle states (starting, running, idle, error, stopping)
- Design state persistence for recovery
- Plan state synchronization between agent instances

### Monitoring & Health Check Design
- Health check endpoint/mechanism specification
- Performance metrics collection
- Alert thresholds and escalation procedures
- Log aggregation and analysis

## Phase 2: Agent Testing Strategy

### Agent Testing Levels
**Unit Tests**: Individual agent functions and methods
**Integration Tests**: Agent communication with other agents
**System Tests**: Full workflow testing in tmux/container environment
**Chaos Tests**: Agent behavior under failure conditions

### Test Environment Setup
- Mock agent dependencies
- Simulated tmux sessions for testing
- Redis test instances for pub/sub testing
- Automated test execution in both host/container modes

## Phase 3: Task Planning Approach
*This section describes what the agent_tasks command will do - DO NOT execute during agent_plan*

**Agent Task Generation Strategy**:
- Load agent-spec-template.md as base
- Generate tasks from Phase 1 design docs
- Each communication contract → integration test task [P]
- Each monitoring requirement → health check implementation [P]
- Agent-specific implementation tasks

**Agent Task Ordering Strategy**:
- Setup → Tests → Core Agent Logic → Communication → Monitoring → Integration
- Host-based and containerized versions in parallel [P]
- Dependencies: Tests before implementation, communication before monitoring

**Estimated Output**: 20-25 numbered, ordered agent tasks in tasks.md

**IMPORTANT**: This phase is executed by the agent_tasks command, NOT by agent_plan

## Phase 4: Agent Deployment Strategy

### Host-Based Deployment
- Integration with existing tmux session management
- Agent startup scripts and session initialization
- Configuration management and environment setup

### Containerized Deployment
- Docker container specification for agent
- Integration with docker-compose.containerized.yml
- Volume mounts for persistent agent state

### Hybrid Deployment
- Agents that can operate in both modes
- Runtime mode detection and adaptation
- Configuration switching between tmux/Redis communication

## Complexity Tracking

### Agent Implementation Complexity
- **Communication Logic**: Medium (established patterns exist)
- **Autonomous Operation**: High (requires robust error handling)
- **Multi-Mode Support**: High (host + container compatibility)
- **Testing Coverage**: Medium (test frameworks available)

### Integration Complexity
- **Existing Agent Coordination**: Low (patterns established)
- **Tmux Session Management**: Low (tmux_utils.py available)
- **Container Orchestration**: Medium (Docker infrastructure exists)

## Progress Tracking

### Agent Development Milestones
- [ ] Phase 0: Research completed, frameworks selected
- [ ] Phase 1: Communication contracts defined
- [ ] Phase 1: Monitoring strategy implemented
- [ ] Phase 2: Test framework established
- [ ] Phase 3: Agent tasks generated (agent_tasks command)
- [ ] Phase 4: Host-based agent implemented
- [ ] Phase 4: Containerized agent implemented
- [ ] Phase 5: Integration testing completed
- [ ] Phase 6: Production deployment ready

### Quality Gates
- [ ] Agent operates autonomously for 24+ hours without intervention
- [ ] Agent recovers from common failure scenarios
- [ ] Agent communication follows established protocols
- [ ] Agent passes all automated tests in both deployment modes

---

*Generated by Tmux Orchestrator Spec Kit Integration*
*Specialized for autonomous agent development workflows*