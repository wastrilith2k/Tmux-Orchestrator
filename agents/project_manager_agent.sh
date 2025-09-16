#!/bin/bash

# Project Manager Agent for Tmux Orchestrator
# Follows CLAUDE.md architecture for coordination and quality assurance

PROJECT_NAME="$1"
PROJECT_PATH="$2"
SESSION_NAME="$3"
CYCLE_COUNT=0
LAST_COMMIT_TIME=$(date +%s)
COMMIT_INTERVAL=1800  # 30 minutes

log_activity() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] PROJECT_MANAGER [$PROJECT_NAME]: $1" | tee -a "${PROJECT_PATH}/project_manager.log"
}

coordinate_team() {
    # Check engineer agent status
    local engineer_status=$(tmux capture-pane -t "${SESSION_NAME}" -p | tail -5)

    # Assess work quality and progress
    cd "$PROJECT_PATH"
    local recent_commits=$(git log --oneline -5 2>/dev/null || echo "No commits yet")
    local file_changes=$(git status --porcelain 2>/dev/null | wc -l)

    log_activity "Team Status: Files changed: $file_changes, Recent commits: $(echo "$recent_commits" | wc -l)"

    # Quality checks
    if [ -f "package.json" ]; then
        # Node.js project checks
        if ! npm list --depth=0 &>/dev/null; then
            log_activity "QUALITY ISSUE: Dependency problems detected"
            # Send message to engineer using existing system
            /home/james/projs/Tmux-Orchestrator/send-claude-message.sh "${SESSION_NAME}:0" "PM ALERT: Dependency problems detected. Please run 'npm install' to fix dependencies."
        fi
    elif [ -f "requirements.txt" ]; then
        # Python project checks
        if ! python3 -m py_compile *.py &>/dev/null; then
            log_activity "QUALITY ISSUE: Python syntax errors detected"
            # Send message to engineer using existing system
            /home/james/projs/Tmux-Orchestrator/send-claude-message.sh "${SESSION_NAME}:0" "PM ALERT: Python syntax errors detected. Please review and fix code syntax."
        fi
    fi

    # Send coordination message to engineer if needed
    if [ $file_changes -gt 10 ]; then
        log_activity "COORDINATION: Many changes detected, suggesting commit"
        /home/james/projs/Tmux-Orchestrator/send-claude-message.sh "${SESSION_NAME}:0" "PM GUIDANCE: Consider committing current changes - $file_changes files modified"
    fi
}

enforce_git_discipline() {
    cd "$PROJECT_PATH"
    local current_time=$(date +%s)
    local time_since_commit=$((current_time - LAST_COMMIT_TIME))

    if [ $time_since_commit -gt $COMMIT_INTERVAL ]; then
        if [ -n "$(git status --porcelain)" ]; then
            git add -A
            git commit -m "PM-Enforced: Progress checkpoint after ${time_since_commit}s"
            LAST_COMMIT_TIME=$current_time
            log_activity "ENFORCED GIT DISCIPLINE: Committed changes after $((time_since_commit/60)) minutes"
        fi
    fi
}

manage_project_lifecycle() {
    cd "$PROJECT_PATH"

    # Project analysis and planning
    if [ ! -f ".project_phase" ]; then
        echo "initialization" > .project_phase
        log_activity "PROJECT LIFECYCLE: Starting initialization phase"
    fi

    local current_phase=$(cat .project_phase)
    case $current_phase in
        "initialization")
            if [ -n "$(ls -A)" ] && [ -f "README.md" ]; then
                echo "development" > .project_phase
                log_activity "PROJECT LIFECYCLE: Advanced to development phase"
            fi
            ;;
        "development")
            local commit_count=$(git rev-list --count HEAD 2>/dev/null || echo "0")
            if [ $commit_count -gt 5 ]; then
                echo "testing" > .project_phase
                log_activity "PROJECT LIFECYCLE: Advanced to testing phase"
            fi
            ;;
        "testing")
            # Future: implement testing validation
            log_activity "PROJECT LIFECYCLE: In testing phase"
            ;;
    esac
}

update_orchestrator_status() {
    # Report to orchestrator
    local status_report="PM-$PROJECT_NAME: Cycle $CYCLE_COUNT, Phase $(cat "$PROJECT_PATH/.project_phase" 2>/dev/null || echo 'unknown')"
    echo "$status_report" > "/tmp/pm_status_${PROJECT_NAME}.txt"

    # Update hub API if available
    if curl -s http://localhost:8080/health &>/dev/null; then
        local project_id=$(cat "$PROJECT_PATH/.project_id" 2>/dev/null || echo "unknown")
        if [ "$project_id" != "unknown" ]; then
            curl -s -X PUT "http://localhost:8080/api/projects/$project_id" \
                -H "Content-Type: application/json" \
                -d "{\"status\": \"managed\", \"manager_cycle\": $CYCLE_COUNT}" &>/dev/null
        fi
    fi
}

main_coordination_loop() {
    while true; do
        CYCLE_COUNT=$((CYCLE_COUNT + 1))

        log_activity "=== PROJECT MANAGER CYCLE #$CYCLE_COUNT ==="

        # Core PM responsibilities
        coordinate_team
        enforce_git_discipline
        manage_project_lifecycle
        update_orchestrator_status

        log_activity "Cycle #$CYCLE_COUNT complete - next in 60 seconds"
        sleep 60
    done
}

# Validate inputs
if [ -z "$PROJECT_NAME" ] || [ -z "$PROJECT_PATH" ] || [ -z "$SESSION_NAME" ]; then
    echo "Usage: $0 <project_name> <project_path> <session_name>"
    exit 1
fi

if [ ! -d "$PROJECT_PATH" ]; then
    echo "Error: Project path $PROJECT_PATH does not exist"
    exit 1
fi

log_activity "Project Manager starting for $PROJECT_NAME at $PROJECT_PATH"
log_activity "Managing session: $SESSION_NAME"

# Start coordination loop
main_coordination_loop

