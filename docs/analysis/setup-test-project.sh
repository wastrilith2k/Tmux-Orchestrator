#!/bin/bash

# Simple Project Setup and Test Script
# This script will test the enhanced orchestrator with a basic project

set -e  # Exit on any error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config/orchestrator.conf"

echo "🚀 Starting Tmux Orchestrator Test with Simple Project"
echo "======================================================"

# Test 1: Validate our fixes work
echo "📋 Test 1: Validating enhanced scripts..."

# Test the schedule script with validation
echo "  Testing schedule_with_note.sh..."
if ./schedule_with_note.sh 0.1 "Test validation" "nonexistent:0" 2>/dev/null; then
    echo "  ❌ FAIL: Schedule script should have rejected nonexistent session"
    exit 1
else
    echo "  ✅ PASS: Schedule script correctly validates sessions"
fi

# Test the message script with validation
echo "  Testing send-claude-message.sh..."
if ./send-claude-message.sh "nonexistent:0" "test message" 2>/dev/null; then
    echo "  ❌ FAIL: Message script should have rejected nonexistent session"
    exit 1
else
    echo "  ✅ PASS: Message script correctly validates sessions"
fi

echo "📋 Test 2: Setting up simple test project..."

# Create a simple test project
TEST_PROJECT_DIR="$HOME/test-simple-project"
mkdir -p "$TEST_PROJECT_DIR"

cat > "$TEST_PROJECT_DIR/package.json" << 'EOF'
{
  "name": "simple-test-app",
  "version": "1.0.0",
  "description": "Simple test project for Tmux Orchestrator",
  "main": "app.js",
  "scripts": {
    "start": "node app.js",
    "dev": "node app.js"
  },
  "dependencies": {}
}
EOF

cat > "$TEST_PROJECT_DIR/app.js" << 'EOF'
console.log('Simple test app is running!');
console.log('Current time:', new Date().toISOString());

// Simple HTTP server
const http = require('http');
const server = http.createServer((req, res) => {
  res.writeHead(200, {'Content-Type': 'text/plain'});
  res.end('Hello from Simple Test App!\n');
});

const port = 3000;
server.listen(port, () => {
  console.log(`Server running at http://localhost:${port}/`);
});
EOF

cat > "$TEST_PROJECT_DIR/README.md" << 'EOF'
# Simple Test Project

This is a minimal Node.js project for testing the Tmux Orchestrator.

## Tasks to Complete:
1. Add a /status endpoint that returns JSON with current time
2. Add basic error handling for the server
3. Create a simple HTML response for the root path
4. Add environment variable support for the port

## Success Criteria:
- Server starts without errors
- /status endpoint returns valid JSON
- Basic error handling prevents crashes
- Port is configurable via environment variable
EOF

echo "  ✅ Created simple test project at $TEST_PROJECT_DIR"

echo "📋 Test 3: Starting orchestrator session..."

# Kill any existing test session
tmux kill-session -t "simple-test" 2>/dev/null || true

# Create new session for our test
tmux new-session -d -s "simple-test" -c "$TEST_PROJECT_DIR"
tmux rename-window -t "simple-test:0" "Claude-Agent"

# Create additional windows
tmux new-window -t "simple-test" -n "Dev-Server" -c "$TEST_PROJECT_DIR"
tmux new-window -t "simple-test" -n "Shell" -c "$TEST_PROJECT_DIR"

echo "  ✅ Created tmux session 'simple-test' with 3 windows"

echo "📋 Test 4: Testing enhanced communication..."

# Test our enhanced message script
echo "  Testing message logging..."
./send-claude-message.sh "simple-test:0" "Hello! You are a helpful AI agent working on a simple Node.js project."

# Check if log was created
if [ -f "logs/communications/messages-$(date +%Y%m%d).log" ]; then
    echo "  ✅ Message logging is working"
    echo "  Last log entry:"
    tail -1 "logs/communications/messages-$(date +%Y%m%d).log" | sed 's/^/    /'
else
    echo "  ❌ Message logging failed"
fi

echo "📋 Test 5: Testing self-scheduling..."

# Test scheduling with our session
./schedule_with_note.sh 0.5 "Test check-in for simple project" "simple-test:0"
echo "  ✅ Scheduled test check-in (will trigger in 30 seconds)"

echo ""
echo "🎉 Setup Complete! Test Environment Ready"
echo "========================================"
echo ""
echo "Your test environment is ready:"
echo "  📁 Project: $TEST_PROJECT_DIR"
echo "  📺 Session: simple-test"
echo "  📝 Logs: logs/"
echo ""
echo "Next steps:"
echo "1. Attach to the session: tmux attach-session -t simple-test"
echo "2. Start Claude in window 0 and give it the project briefing"
echo "3. Watch the enhanced logging in action"
echo ""
echo "To clean up later:"
echo "  tmux kill-session -t simple-test"
echo "  rm -rf $TEST_PROJECT_DIR"
echo ""
echo "Enhanced features now available:"
echo "  ✅ Portable paths (no more hard-coded locations)"
echo "  ✅ Session/window validation before actions"
echo "  ✅ Comprehensive message logging"
echo "  ✅ Better error messages and debugging"
echo "  ✅ Self-scheduling with validation"