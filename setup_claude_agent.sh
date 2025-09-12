#!/bin/bash

# Setup Claude Agent with Pre-configured Approval Settings
# Usage: ./setup_claude_agent.sh <project_path> [session_name]

set -e

PROJECT_PATH="$1"
SESSION_NAME="${2:-$(basename "$PROJECT_PATH")}"
CLAUDE_CONFIG_SOURCE="$HOME/.claude"
CLAUDE_CONFIG_TARGET="$HOME/.claude-agent-$SESSION_NAME"

if [ -z "$PROJECT_PATH" ]; then
    echo "Usage: $0 <project_path> [session_name]"
    echo "Example: $0 /home/james/test-project my-agent"
    exit 1
fi

if [ ! -d "$PROJECT_PATH" ]; then
    echo "Error: Project path '$PROJECT_PATH' does not exist"
    exit 1
fi

echo "Setting up Claude agent for project: $PROJECT_PATH"
echo "Session name: $SESSION_NAME"

# Create agent-specific Claude configuration directory
if [ -d "$CLAUDE_CONFIG_TARGET" ]; then
    echo "Backing up existing agent config..."
    mv "$CLAUDE_CONFIG_TARGET" "$CLAUDE_CONFIG_TARGET.backup.$(date +%s)"
fi

echo "Copying Claude configuration..."
cp -r "$CLAUDE_CONFIG_SOURCE" "$CLAUDE_CONFIG_TARGET"

# Create project-specific configuration with pre-approved tools
PROJECT_KEY="$PROJECT_PATH"
CONFIG_FILE="$CLAUDE_CONFIG_TARGET.json"

# Copy main config and modify for this agent
cp "$HOME/.claude.json" "$CONFIG_FILE"

# Use python to modify the JSON configuration
python3 - << EOF
import json
import os

config_file = "$CONFIG_FILE"
project_path = "$PROJECT_PATH"

# Load existing config
with open(config_file, 'r') as f:
    config = json.load(f)

# Ensure projects section exists
if 'projects' not in config:
    config['projects'] = {}

# Add/update project configuration with pre-approved tools
config['projects'][project_path] = {
    "allowedTools": [
        "Bash",
        "ReadFile", 
        "WriteFile",
        "KillBash",
        "BashOutput"
    ],
    "history": [],
    "mcpContextUris": [],
    "mcpServers": {},
    "enabledMcpjsonServers": [],
    "disabledMcpjsonServers": [],
    "hasTrustDialogAccepted": True,
    "projectOnboardingSeenCount": 1,
    "hasClaudeMdExternalIncludesApproved": True,
    "hasClaudeMdExternalIncludesWarningShown": True,
    "autoApproveCommands": {
        # HTTP/API Testing
        "curl": True,
        "wget": True,
        "http": True,
        
        # Node.js Development
        "node": True,
        "npm": True,
        "npx": True,
        "yarn": True,
        "pnpm": True,
        
        # Python Development
        "python": True,
        "python3": True,
        "pip": True,
        "pip3": True,
        "pytest": True,
        
        # Environment Variables
        "PORT": True,
        "NODE_ENV": True,
        "DEBUG": True,
        "API_KEY": True,
        
        # Development Servers
        "serve": True,
        "dev": True,
        "start": True,
        "build": True,
        "test": True,
        
        # File Operations
        "ls": True,
        "cat": True,
        "head": True,
        "tail": True,
        "grep": True,
        "find": True,
        
        # Git Operations
        "git": True,
        
        # Process Management
        "ps": True,
        "kill": True,
        "killall": True,
        
        # Network/Localhost patterns
        "curl_localhost": True,
        "localhost": True,
        
        # Common port testing
        "curl_3000": True,
        "curl_8080": True,
        "curl_5000": True,
        
        # Development workflows
        "exact_curl_http___localhost_3000_": True,
        "exact_curl_http___localhost_8080_": True,
        "exact_PORT_8080_node_app_js": True,
        "exact_npm_start": True,
        "exact_npm_run_dev": True,
        "exact_node_app_js": True
    }
}

# Save modified config
with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print(f"Updated configuration for project: {project_path}")
EOF

echo "✅ Claude agent configuration created at: $CLAUDE_CONFIG_TARGET"
echo "✅ Modified configuration file: $CONFIG_FILE"

# Create environment script for starting Claude with this config
ENV_SCRIPT="$HOME/.claude-env-$SESSION_NAME.sh"
cat > "$ENV_SCRIPT" << EOF
#!/bin/bash
# Claude Agent Environment for $SESSION_NAME
export CLAUDE_CONFIG_DIR="$CLAUDE_CONFIG_TARGET"
export CLAUDE_CONFIG_FILE="$CONFIG_FILE"
export PROJECT_PATH="$PROJECT_PATH"

# Start Claude with agent-specific configuration
cd "$PROJECT_PATH"
CLAUDE_CONFIG="\$CLAUDE_CONFIG_FILE" claude
EOF

chmod +x "$ENV_SCRIPT"

echo "✅ Environment script created: $ENV_SCRIPT"
echo ""
echo "To start Claude agent with pre-configured approvals:"
echo "  $ENV_SCRIPT"
echo ""
echo "Or manually:"
echo "  cd $PROJECT_PATH"
echo "  CLAUDE_CONFIG='$CONFIG_FILE' claude"
