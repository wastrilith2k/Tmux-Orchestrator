# Testing GitHub Spec Kit Integration with Tmux Orchestrator

This script demonstrates the Spec Kit integration by creating a sample feature specification,
implementation plan, and tasks breakdown.

## Example 1: Standard Feature Development

### Step 1: Create Feature Specification
```bash
./bin/spec-kit-commands.sh specify "AI-powered code review agent that analyzes pull requests and provides automated feedback"
```

Expected output:
- Creates `specs/001-ai-powered-code-review/spec.md`
- Feature specification with user stories and requirements
- Ready for implementation planning

### Step 2: Generate Implementation Plan
```bash
./bin/spec-kit-commands.sh plan "Python FastAPI service with GitHub API integration, OpenAI for analysis, PostgreSQL for results storage, Redis for caching"
```

Expected output:
- Creates `specs/001-ai-powered-code-review/plan.md`
- Technical architecture and implementation details
- Supporting documents (research.md, data-model.md)

### Step 3: Generate Executable Tasks
```bash
./bin/spec-kit-commands.sh tasks
```

Expected output:
- Creates `specs/001-ai-powered-code-review/tasks.md`
- Numbered tasks (T001, T002, ...) with dependencies
- Parallel execution markers [P] for independent tasks

## Example 2: Agent-Specific Development

### Step 1: Create Agent Specification
```bash
./bin/spec-kit-commands.sh agent_specify "Autonomous monitoring agent that tracks system health and alerts on issues"
```

Expected output:
- Agent-focused specification with autonomous operation requirements
- Inter-agent communication protocols
- Error recovery and health check specifications

### Step 2: Generate Agent Implementation Plan
```bash
./bin/spec-kit-commands.sh agent_plan "Python containerized agent with Redis pub/sub, tmux fallback communication, 24/7 operation capability"
```

Expected output:
- Dual deployment strategy (host-based + containerized)
- Agent communication contracts
- Health monitoring and recovery procedures

### Step 3: Generate Agent Tasks
```bash
./bin/spec-kit-commands.sh agent_tasks
```

Expected output:
- Agent-specific tasks with AT### prefixes
- Both host-based (.sh) and containerized (.py) implementation tasks
- Communication, monitoring, and integration tasks

## Benefits Demonstrated

1. **Structured Thinking**: Clear progression from idea to executable tasks
2. **Quality Assurance**: Templates enforce completeness and testability
3. **Parallel Execution**: Independent tasks can run simultaneously
4. **Agent Integration**: Specialized workflows for autonomous agent development
5. **Documentation**: Complete audit trail and decision record

## Integration with Existing Systems

The Spec Kit integration works seamlessly with existing Tmux Orchestrator components:
- Agents can use SDD commands during autonomous operation
- Generated tasks integrate with existing communication protocols
- Both tmux-based and containerized deployments supported
- Compatible with existing quality assurance and git workflows