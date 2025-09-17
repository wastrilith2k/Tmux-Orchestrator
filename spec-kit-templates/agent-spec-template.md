# Agent Specification Template
# Adapted from GitHub Spec Kit for Tmux Orchestrator Autonomous Agents

**Feature Branch**: `[###-feature-name]`
**Created**: [DATE]
**Status**: Draft
**Agent**: [AGENT_NAME]
**Input**: Agent description: "$ARGUMENTS"

## Execution Flow (agent_main)
```
1. Parse agent task description from Input
   → If empty: ERROR "No feature description provided"
2. Extract key concepts from description
   → Identify: actors, actions, data, constraints, automation requirements
3. For each unclear aspect:
   → Mark with [NEEDS CLARIFICATION: specific question]
4. Fill Agent Scenarios & Testing section
   → If no clear agent workflow: ERROR "Cannot determine agent scenarios"
5. Generate Functional Requirements for autonomous operation
   → Each requirement must be testable and automatable
   → Mark ambiguous requirements
6. Identify Key Entities (if data involved)
7. Identify Integration Points with other agents
8. Run Review Checklist
   → If any [NEEDS CLARIFICATION]: WARN "Spec has uncertainties"
   → If implementation details found: ERROR "Remove tech details"
9. Return: SUCCESS (spec ready for autonomous planning)
```

---

## ⚡ Quick Guidelines

### Agent-Specific Focus
- **Autonomous Operation**: All requirements must be executable without human intervention
- **Inter-Agent Communication**: Clear protocols for agent coordination
- **Error Recovery**: Graceful handling of failures and recovery procedures
- **Monitoring**: Built-in status reporting and health checks

### Section Requirements
- **Mandatory sections**: Must be completed for every agent feature
- **Optional sections**: Include only when relevant to the feature
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

### For AI Agent Generation
When creating this spec from an agent task prompt:
1. **Mark all ambiguities**: Use [NEEDS CLARIFICATION: specific question] for any assumption
2. **Think autonomously**: Every requirement must be executable by an agent without human input
3. **Consider agent coordination**: How will this agent communicate with others?
4. **Plan for failures**: What happens when things go wrong?

---

## Agent Scenarios & Testing *(mandatory)*

### Primary Agent Stories
**AS-001**: As an autonomous agent, I want to [specific capability] so that [business value]
**AS-002**: As a coordinating agent, I want to [communication need] so that [team efficiency]
**AS-003**: As a monitoring agent, I want to [oversight capability] so that [quality assurance]

### Agent Workflows
```
Workflow 1: [Primary agent operation]
1. Agent receives task/trigger
2. Agent validates preconditions
3. Agent executes core functionality
4. Agent reports status/results
5. Agent schedules next action (if applicable)

Workflow 2: [Inter-agent coordination]
1. Agent A sends message to Agent B
2. Agent B acknowledges and processes
3. Agent B responds with results
4. Agent A validates response
5. Both agents log interaction
```

### Acceptance Criteria
**AC-001**: Agent successfully executes primary workflow without human intervention
**AC-002**: Agent handles error conditions gracefully and reports status
**AC-003**: Agent coordinates with other agents using established protocols
**AC-004**: Agent maintains operation logs for debugging and audit

---

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: Agent MUST [specific autonomous capability, e.g., "process incoming tasks automatically"]
- **FR-002**: Agent MUST [communication requirement, e.g., "send status updates every 30 minutes"]
- **FR-003**: Agent MUST [error handling, e.g., "recover from network failures within 60 seconds"]
- **FR-004**: Agent MUST [data requirement, e.g., "persist operation state for recovery"]
- **FR-005**: Agent MUST [coordination, e.g., "coordinate with other agents via Redis pub/sub"]

*Example of marking unclear requirements:*
- **FR-006**: Agent MUST authenticate via [NEEDS CLARIFICATION: auth method not specified - API key, JWT, certificate?]
- **FR-007**: Agent MUST retry operations [NEEDS CLARIFICATION: retry count and backoff strategy not specified]

### Agent Integration Requirements
- **IR-001**: Agent MUST integrate with tmux session management
- **IR-002**: Agent MUST use established messaging protocols (send-claude-message.sh or Redis)
- **IR-003**: Agent MUST follow git commit patterns (every 30 minutes)
- **IR-004**: Agent MUST implement health check endpoints/mechanisms

### Key Entities *(include if agent involves data)*
- **[Entity 1]**: [What it represents, key attributes for agent processing]
- **[Entity 2]**: [What it represents, relationships to other entities]

### Inter-Agent Communication
- **Message Types**: [List of message types this agent sends/receives]
- **Communication Channels**: [tmux windows, Redis channels, file-based, etc.]
- **Protocol Compliance**: [How agent follows established communication patterns]

---

## Review & Acceptance Checklist
*GATE: Automated checks run during agent_main() execution*

### Agent Quality
- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on autonomous operation and agent coordination
- [ ] Written for agent implementation and monitoring
- [ ] All mandatory sections completed

### Requirement Completeness
- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Requirements are testable and automatable
- [ ] Success criteria are measurable by agents
- [ ] Scope is clearly bounded for autonomous execution
- [ ] Dependencies and assumptions identified
- [ ] Integration points with other agents specified

### Agent-Specific Validation
- [ ] Agent can operate without human intervention
- [ ] Error recovery procedures are defined
- [ ] Communication protocols are specified
- [ ] Monitoring and logging requirements are clear

---

## Execution Status
*Updated by agent_main() during processing*

- [ ] Agent task description parsed
- [ ] Key concepts extracted
- [ ] Ambiguities marked
- [ ] Agent scenarios defined
- [ ] Requirements generated
- [ ] Entities identified
- [ ] Integration points specified
- [ ] Review checklist passed

---

*Generated by Tmux Orchestrator Spec Kit Integration*
*Adapted from GitHub Spec Kit for autonomous agent workflows*