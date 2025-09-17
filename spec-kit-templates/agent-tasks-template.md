# Agent Tasks Template
# Adapted from GitHub Spec Kit for Autonomous Agent Implementation

**Input**: Agent design documents from `/specs/[###-agent-feature]/`
**Prerequisites**: plan.md (required), research.md, communication.md, monitoring.md

## Execution Flow (agent_main)
```
1. Load plan.md and extract agent architecture, deployment modes
2. Load optional agent documents:
   → communication.md: Extract message types → communication tasks
   → monitoring.md: Extract health checks → monitoring tasks
   → recovery.md: Extract error handling → recovery tasks
3. Generate agent tasks by category:
   → Setup: project init, dependencies, configuration
   → Tests: communication tests, integration tests, chaos tests
   → Core: agent logic, state management, autonomous operation
   → Communication: messaging, coordination, status reporting
   → Monitoring: health checks, logging, alerting
   → Integration: tmux integration, container integration
   → Deployment: host-based, containerized, configuration
4. Apply agent task rules:
   → Different deployment modes = mark [P] for parallel
   → Same agent file = sequential (no [P])
   → Tests before implementation (TDD for agents)
5. Number tasks sequentially (AT001, AT002... for Agent Tasks)
6. Generate dependency graph for agent development
7. Create parallel execution examples for dual deployment
8. Validate agent task completeness:
   → All communication contracts have tests?
   → All monitoring requirements implemented?
   → Both host-based and containerized versions?
9. Return: SUCCESS (agent tasks ready for implementation)
```

---

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, different deployment modes)
- Include exact file paths for agent implementations
- **AT### prefix**: Agent Task identification

## Path Conventions
**Agent Structure**:
- **Host-based**: `agents/[agent-name]/host-based/`
- **Containerized**: `agents/[agent-name]/containerized/`
- **Shared**: `agents/[agent-name]/shared/`
- **Tests**: `tests/agents/[agent-name]/`

## Phase 3.1: Agent Setup
- [ ] AT001 Create agent directory structure per implementation plan
- [ ] AT002 Initialize host-based agent shell script framework
- [ ] AT003 [P] Initialize containerized agent Python framework
- [ ] AT004 [P] Configure agent dependencies and environment
- [ ] AT005 [P] Set up agent configuration management (shared/config.json)

## Phase 3.2: Agent Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
- [ ] AT006 [P] Create communication protocol tests in tests/agents/[agent-name]/test_communication.py
- [ ] AT007 [P] Create agent lifecycle tests in tests/agents/[agent-name]/test_lifecycle.py
- [ ] AT008 [P] Create tmux integration tests in tests/agents/[agent-name]/test_tmux_integration.py
- [ ] AT009 [P] Create container integration tests in tests/agents/[agent-name]/test_container_integration.py
- [ ] AT010 [P] Create agent coordination tests in tests/agents/[agent-name]/test_coordination.py
- [ ] AT011 [P] Create error recovery tests in tests/agents/[agent-name]/test_recovery.py
- [ ] AT012 [P] Create health check tests in tests/agents/[agent-name]/test_monitoring.py

## Phase 3.3: Core Agent Implementation (ONLY after tests are failing)
- [ ] AT013 Implement core agent class/functions in agents/[agent-name]/shared/core.py
- [ ] AT014 [P] Implement host-based agent script in agents/[agent-name]/host-based/[agent-name].sh
- [ ] AT015 [P] Implement containerized agent in agents/[agent-name]/containerized/[agent-name].py
- [ ] AT016 [P] Implement agent state management in agents/[agent-name]/shared/state.py
- [ ] AT017 [P] Implement autonomous operation logic per agent specification
- [ ] AT018 [P] Implement agent configuration loading in agents/[agent-name]/shared/config.py

## Phase 3.4: Agent Communication Implementation
- [ ] AT019 [P] Implement tmux messaging in agents/[agent-name]/host-based/communication.sh
- [ ] AT020 [P] Implement Redis pub/sub in agents/[agent-name]/containerized/communication.py
- [ ] AT021 [P] Implement message schemas in agents/[agent-name]/shared/messages.py
- [ ] AT022 [P] Implement inter-agent coordination protocols
- [ ] AT023 [P] Implement status reporting mechanisms

## Phase 3.5: Agent Monitoring & Health Implementation
- [ ] AT024 [P] Implement health checks in agents/[agent-name]/*/monitoring.*
- [ ] AT025 [P] Implement agent logging and audit trails
- [ ] AT026 [P] Implement performance metrics collection
- [ ] AT027 [P] Implement error detection and alerting
- [ ] AT028 [P] Implement recovery procedures per recovery.md

## Phase 3.6: Agent Integration
- [ ] AT029 Integrate agent with tmux_utils.py for session management
- [ ] AT030 [P] Integrate agent with existing orchestrator systems
- [ ] AT031 [P] Integrate agent with container orchestration (docker-compose)
- [ ] AT032 [P] Configure agent deployment scripts (bin/setup_[agent-name]_agent.sh)

## Phase 3.7: Agent Testing & Validation
- [ ] AT033 [P] Run full agent test suite in host-based mode
- [ ] AT034 [P] Run full agent test suite in containerized mode
- [ ] AT035 [P] Perform agent chaos testing (network failures, resource limits)
- [ ] AT036 [P] Validate agent coordination with other existing agents
- [ ] AT037 [P] Perform 24-hour autonomous operation test

## Phase 3.8: Agent Documentation & Polish
- [ ] AT038 [P] Create agent operation documentation
- [ ] AT039 [P] Add agent to main project documentation (docs/PROJECT_STRUCTURE.md)
- [ ] AT040 [P] Create agent troubleshooting guide
- [ ] AT041 [P] Implement agent performance optimizations
- [ ] AT042 [P] Add agent examples and usage patterns

## Dependencies
- Setup (AT001-AT005) before all other phases
- Tests (AT006-AT012) before implementation (AT013-AT018)
- Core implementation (AT013-AT018) before communication (AT019-AT023)
- Communication (AT019-AT023) before monitoring (AT024-AT028)
- All implementation before integration (AT029-AT032)
- Integration before testing (AT033-AT037)
- Testing before documentation (AT038-AT042)

## Parallel Execution Examples

### Setup Phase (can run together)
```bash
# Launch AT002-AT005 together:
Task: "Initialize host-based agent shell script framework"
Task: "Initialize containerized agent Python framework"
Task: "Configure agent dependencies and environment"
Task: "Set up agent configuration management"
```

### Test Creation Phase (all parallel)
```bash
# Launch AT006-AT012 together (different test files):
Task: "Create communication protocol tests in tests/agents/[name]/test_communication.py"
Task: "Create agent lifecycle tests in tests/agents/[name]/test_lifecycle.py"
Task: "Create tmux integration tests in tests/agents/[name]/test_tmux_integration.py"
Task: "Create container integration tests in tests/agents/[name]/test_container_integration.py"
# ... all test files are independent
```

### Implementation Phase (deployment modes parallel)
```bash
# Launch AT014-AT015 together (different deployment modes):
Task: "Implement host-based agent script in agents/[name]/host-based/[name].sh"
Task: "Implement containerized agent in agents/[name]/containerized/[name].py"
```

## Agent-Specific Validation Rules
*Applied during agent_main() execution*

1. **Dual Implementation**:
   - Each agent MUST have both host-based (.sh) and containerized (.py) versions
   - Both versions must implement the same agent specification

2. **Communication Compliance**:
   - Host-based agents MUST use send-claude-message.sh
   - Containerized agents MUST use Redis pub/sub
   - Message schemas MUST be consistent between modes

3. **Autonomous Operation**:
   - Agents MUST operate without human intervention
   - Agents MUST implement error recovery procedures
   - Agents MUST provide health check mechanisms

4. **Integration Requirements**:
   - Agents MUST integrate with existing tmux_utils.py
   - Agents MUST follow established git commit patterns
   - Agents MUST implement status reporting every 30 minutes

## Validation Checklist
*GATE: Checked by agent_main() before returning*

- [ ] All communication contracts have corresponding tests
- [ ] All monitoring requirements have implementation tasks
- [ ] Both host-based and containerized versions are planned
- [ ] All tests come before implementation tasks
- [ ] Parallel tasks are truly independent (different files/modes)
- [ ] Each task specifies exact file path
- [ ] No task modifies same file as another [P] task
- [ ] Agent follows autonomous operation principles
- [ ] Integration with existing systems is planned
- [ ] 24-hour operation test is included

## Notes
- **[P] tasks**: Different files or deployment modes, no dependencies
- **AT### numbering**: Unique agent task identification
- **Dual implementation**: Host-based + containerized versions required
- **Autonomous focus**: All tasks must support unattended operation
- **Integration compliance**: Must work with existing Tmux Orchestrator systems

---

*Generated by Tmux Orchestrator Spec Kit Integration*
*Specialized for autonomous agent task breakdown and implementation*