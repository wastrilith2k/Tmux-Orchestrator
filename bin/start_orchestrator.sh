#!/bin/bash
#
# Hub Orchestrator Startup Script
# Starts the automated agent management service
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 Starting Hub Orchestrator Service..."
echo "📍 Working directory: $(pwd)"
echo "⏰ Check interval: 30 seconds"
echo "🎯 Mission: Autonomous agent management"
echo ""

# Check dependencies
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is required but not installed"
    exit 1
fi

if ! command -v tmux &> /dev/null; then
    echo "❌ Error: tmux is required but not installed"
    exit 1
fi

# Check if hub API is running
if ! curl -s http://localhost:8080/health > /dev/null; then
    echo "⚠️  Warning: Hub API (http://localhost:8080) not responding"
    echo "   Make sure the admin system is running:"
    echo "   cd admin-system && docker-compose -f docker-compose.admin.yml up -d"
    echo ""
fi

# Install Python dependencies if needed
if ! python3 -c "import requests" 2>/dev/null; then
    echo "📦 Installing required Python packages..."
    python3 -m pip install requests || echo "⚠️ Could not install requests - trying to continue anyway"
fi

echo "🎯 Launching orchestrator - press Ctrl+C to stop"
echo "📝 Logs will be written to /tmp/hub-orchestrator.log"
echo ""

# Run the orchestrator
python3 hub_orchestrator.py