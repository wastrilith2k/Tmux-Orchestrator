#!/bin/bash
# Spec-Driven Development Commands for Tmux Orchestrator Agents
# Implements /specify, /plan, /tasks commands for autonomous agent development

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Import the Python integration module
PYTHON_MODULE="$PROJECT_ROOT/utils/spec_kit_integration.py"

log_activity() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] SPEC_KIT: $1" | tee -a "${PROJECT_ROOT}/logs/spec_kit.log"
}

# /specify command - Create feature specification from natural language
specify_command() {
    local description="$*"

    if [[ -z "$description" ]]; then
        echo "Error: /specify requires a feature description"
        echo "Usage: /specify <feature description>"
        echo "Example: /specify Real-time chat system with message history"
        return 1
    fi

    log_activity "Starting /specify command: $description"

    # Use Python integration to create specification
    python3 -c "
import sys
sys.path.append('$PROJECT_ROOT')
from utils.spec_kit_integration import SpecKitIntegration
from pathlib import Path

spec_kit = SpecKitIntegration(Path('$PROJECT_ROOT'))
result = spec_kit.specify_command('$description')

print(f'✅ Feature specification created:')
print(f'   Branch: {result[\"branch_name\"]}')
print(f'   Spec file: {result[\"spec_file\"]}')
print(f'   Feature number: {result[\"feature_number\"]}')
print(f'')
print(f'Next step: /plan <technical details>')
"

    log_activity "Completed /specify command"
}

# /plan command - Generate technical implementation plan
plan_command() {
    local technical_details="$*"

    if [[ -z "$technical_details" ]]; then
        echo "Error: /plan requires technical details"
        echo "Usage: /plan <technical implementation details>"
        echo "Example: /plan WebSocket for real-time messaging, PostgreSQL for history, Redis for presence"
        return 1
    fi

    # Find the most recent feature branch
    local latest_branch=$(find "$PROJECT_ROOT/specs" -maxdepth 1 -type d -name "*-*" 2>/dev/null | sort | tail -1)
    if [[ -n "$latest_branch" ]]; then
        latest_branch=$(basename "$latest_branch")
    fi

    if [[ -z "$latest_branch" ]]; then
        echo "Error: No feature specification found. Run /specify first."
        return 1
    fi

    log_activity "Starting /plan command for $latest_branch: $technical_details"

    # Use Python integration to create implementation plan
    python3 -c "
import sys
sys.path.append('$PROJECT_ROOT')
from utils.spec_kit_integration import SpecKitIntegration
from pathlib import Path

spec_kit = SpecKitIntegration(Path('$PROJECT_ROOT'))
result = spec_kit.plan_command('$latest_branch', '$technical_details')

print(f'✅ Implementation plan created:')
print(f'   Branch: {result[\"branch_name\"]}')
print(f'   Plan file: {result[\"plan_file\"]}')
print(f'   Research file: {result[\"research_file\"]}')
print(f'')
print(f'Next step: /tasks')
"

    log_activity "Completed /plan command for $latest_branch"
}

# /tasks command - Generate executable, dependency-ordered tasks
tasks_command() {
    # Find the most recent feature branch
    local latest_branch=$(find "$PROJECT_ROOT/specs" -maxdepth 1 -type d -name "*-*" 2>/dev/null | sort | tail -1)
    if [[ -n "$latest_branch" ]]; then
        latest_branch=$(basename "$latest_branch")
    fi

    if [[ -z "$latest_branch" ]]; then
        echo "Error: No feature specification found. Run /specify first."
        return 1
    fi

    # Check if plan exists
    if [[ ! -f "$PROJECT_ROOT/specs/$latest_branch/plan.md" ]]; then
        echo "Error: No implementation plan found. Run /plan first."
        return 1
    fi

    log_activity "Starting /tasks command for $latest_branch"

    # Use Python integration to create tasks breakdown
    python3 -c "
import sys
sys.path.append('$PROJECT_ROOT')
from utils.spec_kit_integration import SpecKitIntegration
from pathlib import Path

spec_kit = SpecKitIntegration(Path('$PROJECT_ROOT'))
result = spec_kit.tasks_command('$latest_branch')

print(f'✅ Tasks breakdown created:')
print(f'   Branch: {result[\"branch_name\"]}')
print(f'   Tasks file: {result[\"tasks_file\"]}')
print(f'')
print(f'Tasks are ready for agent execution!')
print(f'View tasks: cat {result[\"tasks_file\"]}')
"

    log_activity "Completed /tasks command for $latest_branch"
}

# Agent-specific commands for autonomous development

# /agent_specify - Create agent specification for autonomous agent development
agent_specify_command() {
    local agent_description="$*"

    if [[ -z "$agent_description" ]]; then
        echo "Error: /agent_specify requires an agent description"
        echo "Usage: /agent_specify <agent task description>"
        echo "Example: /agent_specify Autonomous QA agent that runs tests and reports quality metrics"
        return 1
    fi

    log_activity "Starting /agent_specify command: $agent_description"

    # Create agent-specific specification
    python3 -c "
import sys
sys.path.append('$PROJECT_ROOT')
from utils.spec_kit_integration import TmuxSpecKitAgent
from pathlib import Path

agent = TmuxSpecKitAgent(Path('$PROJECT_ROOT'), 'SpecKitAgent')
result = agent.start_new_feature('$agent_description')

print(f'✅ Agent specification created:')
print(f'   Branch: {result[\"branch_name\"]}')
print(f'   Spec file: {result[\"spec_file\"]}')
print(f'')
print(f'Next step: /agent_plan <technical details>')
"

    log_activity "Completed /agent_specify command"
}

# /agent_plan - Generate agent implementation plan
agent_plan_command() {
    local technical_details="$*"

    if [[ -z "$technical_details" ]]; then
        echo "Error: /agent_plan requires technical details"
        echo "Usage: /agent_plan <agent implementation details>"
        echo "Example: /agent_plan Python-based containerized agent with Redis communication and tmux fallback"
        return 1
    fi

    log_activity "Starting /agent_plan command: $technical_details"

    python3 -c "
import sys
sys.path.append('$PROJECT_ROOT')
from utils.spec_kit_integration import TmuxSpecKitAgent
from pathlib import Path

agent = TmuxSpecKitAgent(Path('$PROJECT_ROOT'), 'SpecKitAgent')
# Find latest feature branch automatically
latest_branch = sorted([d.name for d in (Path('$PROJECT_ROOT') / 'specs').iterdir() if d.is_dir() and '-' in d.name])[-1]
agent.current_feature = latest_branch

result = agent.create_implementation_plan('$technical_details')

print(f'✅ Agent implementation plan created:')
print(f'   Branch: {result[\"branch_name\"]}')
print(f'   Plan file: {result[\"plan_file\"]}')
print(f'')
print(f'Next step: /agent_tasks')
"

    log_activity "Completed /agent_plan command"
}

# /agent_tasks - Generate agent-specific executable tasks
agent_tasks_command() {
    log_activity "Starting /agent_tasks command"

    python3 -c "
import sys
sys.path.append('$PROJECT_ROOT')
from utils.spec_kit_integration import TmuxSpecKitAgent
from pathlib import Path

agent = TmuxSpecKitAgent(Path('$PROJECT_ROOT'), 'SpecKitAgent')
# Find latest feature branch automatically
latest_branch = sorted([d.name for d in (Path('$PROJECT_ROOT') / 'specs').iterdir() if d.is_dir() and '-' in d.name])[-1]
agent.current_feature = latest_branch

result = agent.generate_tasks()

print(f'✅ Agent tasks breakdown created:')
print(f'   Branch: {result[\"branch_name\"]}')
print(f'   Tasks file: {result[\"tasks_file\"]}')
print(f'')
print(f'Agent tasks are ready for autonomous execution!')
print(f'View tasks: cat {result[\"tasks_file\"]}')
"

    log_activity "Completed /agent_tasks command"
}

# Command dispatcher
case "$1" in
    "specify")
        shift
        specify_command "$@"
        ;;
    "plan")
        shift
        plan_command "$@"
        ;;
    "tasks")
        shift
        tasks_command "$@"
        ;;
    "agent_specify")
        shift
        agent_specify_command "$@"
        ;;
    "agent_plan")
        shift
        agent_plan_command "$@"
        ;;
    "agent_tasks")
        shift
        agent_tasks_command "$@"
        ;;
    *)
        echo "Spec-Driven Development Commands for Tmux Orchestrator"
        echo ""
        echo "Standard Commands (based on GitHub Spec Kit):"
        echo "  /specify <description>     - Create feature specification from natural language"
        echo "  /plan <tech details>       - Generate technical implementation plan"
        echo "  /tasks                     - Generate executable, dependency-ordered tasks"
        echo ""
        echo "Agent Commands (specialized for autonomous agents):"
        echo "  /agent_specify <description> - Create agent specification for autonomous development"
        echo "  /agent_plan <tech details>   - Generate agent implementation plan"
        echo "  /agent_tasks                 - Generate agent-specific executable tasks"
        echo ""
        echo "Examples:"
        echo "  $0 specify Real-time chat system with message history"
        echo "  $0 plan WebSocket for messaging, PostgreSQL for history, Redis for presence"
        echo "  $0 tasks"
        echo ""
        echo "  $0 agent_specify Autonomous QA agent with testing and quality reporting"
        echo "  $0 agent_plan Python containerized agent with Redis communication"
        echo "  $0 agent_tasks"
        ;;
esac