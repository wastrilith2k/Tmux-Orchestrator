#!/bin/bash

# Entrypoint script for autonomous agent containers
# Initializes the agent environment and starts the appropriate agent type

set -e

echo "🤖 Starting Autonomous Agent Container"
echo "Agent Type: ${AGENT_TYPE}"
echo "Project: ${PROJECT_NAME}"
echo "Workspace: ${PROJECT_PATH}"

# Validate required environment variables
if [ -z "$AGENT_TYPE" ]; then
    echo "❌ ERROR: AGENT_TYPE environment variable is required"
    echo "Valid types: engineer, project-manager, qa-engineer, devops"
    exit 1
fi

if [ -z "$PROJECT_NAME" ]; then
    echo "❌ ERROR: PROJECT_NAME environment variable is required"
    exit 1
fi

# Ensure workspace directory exists
mkdir -p "$PROJECT_PATH"
cd "$PROJECT_PATH"

# Initialize git repository if not exists
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository in workspace"
    git init
    git config user.name "Autonomous Agent"
    git config user.email "agent@tmux-orchestrator.ai"
fi

# Start tmux session
echo "🖥️  Starting tmux session for agent"
tmux new-session -d -s "agent-session" -c "$PROJECT_PATH"

# Wait for Redis to be available
echo "⏳ Waiting for Redis connection..."
until redis-cli -u "$REDIS_URL" ping > /dev/null 2>&1; do
    sleep 1
done
echo "✅ Redis connected"

# Start the appropriate agent based on type
case "$AGENT_TYPE" in
    "engineer")
        echo "🔧 Starting Engineer Agent"
        exec tmux send-keys -t agent-session "containerized-engineer-agent.py $PROJECT_NAME $PROJECT_PATH" Enter
        ;;
    "project-manager")
        echo "👔 Starting Project Manager Agent"
        exec tmux send-keys -t agent-session "containerized-pm-agent.py $PROJECT_NAME $PROJECT_PATH" Enter
        ;;
    "qa-engineer")
        echo "🧪 Starting QA Engineer Agent"
        exec tmux send-keys -t agent-session "containerized-qa-agent.py $PROJECT_NAME $PROJECT_PATH" Enter
        ;;
    "devops")
        echo "🚀 Starting DevOps Agent"
        exec tmux send-keys -t agent-session "containerized-devops-agent.py $PROJECT_NAME $PROJECT_PATH" Enter
        ;;
    *)
        echo "❌ ERROR: Unknown agent type: $AGENT_TYPE"
        exit 1
        ;;
esac

# Keep container running
echo "🎯 Agent started successfully - keeping container alive"
exec tail -f /dev/null