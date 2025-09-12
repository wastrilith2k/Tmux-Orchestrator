#!/bin/bash

# Demo: Claude Agent Self-Learning Approval System
# This script demonstrates how agents learn from approval decisions

set -e

echo "🤖 Claude Agent Self-Learning Approval System Demo"
echo "================================================"
echo ""

PROJECT_PATH="/home/james/test-simple-project"
SESSION_NAME="learning-demo"

echo "📁 Setting up learning demo with project: $PROJECT_PATH"

# Create agent with enhanced configuration
echo "🔧 Creating Claude agent with learning capabilities..."
./setup_claude_agent.sh "$PROJECT_PATH" "$SESSION_NAME"

echo ""
echo "📋 Initial approval configuration includes:"
echo "   ✅ Basic commands: curl, node, npm, git, etc."
echo "   ✅ Environment variables: PORT, NODE_ENV, etc."
echo "   ✅ Common development patterns"
echo ""

echo "🚀 How the learning system works:"
echo ""
echo "1. 📱 When Claude encounters a new command requiring approval:"
echo "   - System detects the approval dialog"
echo "   - Extracts the command being requested"
echo "   - Automatically selects 'Yes, don't ask again'"
echo "   - Adds the command to the agent's approved list"
echo ""
echo "2. 🧠 Command learning patterns:"
echo "   - Base commands: 'curl' -> approves all curl commands"
echo "   - Environment vars: 'PORT=8080 node app.js' -> approves PORT and node"
echo "   - Exact patterns: Full command strings for precise matching"
echo "   - Host patterns: 'curl localhost' -> approves localhost access"
echo ""
echo "3. 🔄 Future behavior:"
echo "   - Similar commands auto-approved without dialogs"
echo "   - Agent becomes more autonomous over time"
echo "   - Configuration persists across sessions"
echo ""

echo "🔍 To monitor learning in real-time:"
echo "   ./approval_monitor.py --interval 3"
echo ""
echo "📊 To see learned commands for this agent:"
echo "   ./approval_monitor.py --list-commands $SESSION_NAME"
echo ""

echo "🎯 Demo configuration created!"
echo "   Agent config: ~/.claude-agent-$SESSION_NAME.json"
echo "   Environment: ~/.claude-env-$SESSION_NAME.sh"
echo ""

echo "▶️  To start the agent:"
echo "   ~/.claude-env-$SESSION_NAME.sh"
echo ""
echo "The agent will now learn from every approval and become"
echo "progressively more autonomous! 🎉"