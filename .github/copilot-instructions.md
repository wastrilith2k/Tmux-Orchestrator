# Tmux Orchestrator - AI Agent Coding Guide

## Architecture Overview

This is a **multi-agent AI orchestration system** where Claude agents coordinate autonomous development work through tmux sessions. The architecture follows a hierarchical pattern:

```
Orchestrator (coordination/oversight)
├── Project Managers (quality/team coordination)
└── Engineers/Specialists (implementation)
```

**Key Insight**: Each agent runs in its own tmux window, communicating via shell scripts. The system persists work sessions even when disconnected.

## Core Workflow Patterns

### Agent Communication Protocol
**ALWAYS use the dedicated script** - never manual tmux commands:
```bash
./send-claude-message.sh session:window "message content"
```

This handles timing automatically and prevents the common error of premature Enter key sends.

### Self-Scheduling Pattern
Agents schedule their own check-ins for autonomous operation:
```bash
./schedule_with_note.sh 30 "Continue feature implementation" "session:window"
```

### Git Safety Rules (CRITICAL)
Every agent must commit every 30 minutes to prevent work loss:
```bash
git add -A
git commit -m "Progress: specific description of work done"
```

## Essential Tmux Patterns

### Creating Windows with Correct Context
```bash
# ALWAYS specify working directory when creating windows
tmux new-window -t session -n "window-name" -c "/path/to/project"

# Verify you're in the right place
tmux send-keys -t session:window "pwd" Enter
```

### Status Monitoring
```python
# Use tmux_utils.py for programmatic session management
orchestrator = TmuxOrchestrator()
status = orchestrator.get_all_windows_status()  # Full session snapshot
content = orchestrator.capture_window_content(session, window, 50)  # Window output
```

## Critical Files & Responsibilities

- **`send-claude-message.sh`**: Universal agent communication (0.5s timing built-in)
- **`schedule_with_note.sh`**: Self-scheduling for autonomous operation
- **`tmux_utils.py`**: Programmatic tmux control with safety checks
- **`CLAUDE.md`**: Complete agent behavior instructions (717 lines of domain knowledge)

## Project Startup Sequence

When starting any project:
1. Find project: `ls -la ~/Coding/`
2. Create session with project path: `tmux new-session -d -s project-name -c "/path"`
3. Set up standard windows: Claude-Agent, Shell, Dev-Server
4. Brief the agent with specific responsibilities and constraints
5. Agent analyzes project type and starts appropriate dev server

## Anti-Patterns to Avoid

- **Never** create windows without `-c` flag (causes wrong working directory)
- **Never** send commands without checking window contents first
- **Never** assume commands succeeded without capturing output
- **Never** work >1 hour without git commits
- **Never** use raw `tmux send-keys` for agent communication

## Quality Assurance Flow

Project Managers enforce standards through structured verification:
- Test every feature before approval
- Verify git commits are meaningful and frequent
- Ensure cross-agent communication follows templates
- Monitor for technical debt accumulation

## Key Technical Patterns

### Window Content Analysis
```bash
# Check what's currently in a window before sending commands
tmux capture-pane -t session:window -p | tail -50
```

### Error Recovery
```bash
# When commands fail, capture full context
tmux capture-pane -t session:window -S -200 -p
```

### Agent Lifecycle
1. Create with clear role briefing
2. Regular status updates via message script
3. Log complete conversations before termination
4. Proper handoff documentation

This system scales autonomous development by keeping agents focused, communication structured, and work automatically preserved through tmux persistence and mandatory git discipline.