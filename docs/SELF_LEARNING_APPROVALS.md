# Claude Agent Self-Learning Approval System

## Overview

The Tmux Orchestrator now includes a sophisticated self-learning approval system that automatically captures and learns from Claude agent approval decisions. Each time an agent approves a command, the system adds that command pattern to the agent's configuration, eliminating future approval dialogs for similar commands.

## Key Features

### 🧠 Intelligent Command Learning
- **Pattern Recognition**: Extracts commands from approval dialogs using advanced regex patterns
- **Command Categorization**: Learns base commands, environment variables, and exact patterns
- **Automatic Configuration Updates**: Dynamically updates agent configuration files
- **Persistent Learning**: Approved commands persist across agent sessions

### 🔄 Learning Patterns

#### Base Command Learning
```bash
# When approving "curl http://localhost:3000/status"
# Learns: "curl" (approves all curl commands)
```

#### Environment Variable Learning
```bash
# When approving "PORT=8080 node app.js"
# Learns: "PORT" and "node" (approves both patterns)
```

#### Exact Pattern Learning
```bash
# Stores: "exact_curl_http___localhost_3000_status"
# For precise command matching
```

#### Host Pattern Learning
```bash
# When approving localhost commands
# Learns: "curl_localhost", "localhost"
# Approves local development patterns
```

## System Components

### 1. Enhanced Agent Manager (`claude_agent_manager.py`)
- `extract_command_from_approval_dialog()`: Parses approval dialogs to extract commands
- `add_command_to_approved_list()`: Updates agent configuration with learned commands
- `monitor_agent_approvals()`: Enhanced monitoring with learning capabilities

### 2. Setup Script (`setup_claude_agent.sh`)
- Creates agent configurations with comprehensive initial approval lists
- Pre-approves common development commands and patterns
- Sets up agent-specific configuration directories

### 3. Real-time Monitor (`approval_monitor.py`)
- Continuously monitors all Claude agents for approval dialogs
- Provides real-time statistics and logging
- Can run as daemon for autonomous operation

### 4. Demo System (`demo_learning_system.sh`)
- Demonstrates the complete learning workflow
- Shows initial configuration and learning capabilities

## Configuration Structure

### Agent Configuration File
```json
{
  "projects": {
    "/path/to/project": {
      "autoApproveCommands": {
        // Base commands
        "curl": true,
        "node": true,
        "npm": true,

        // Environment variables
        "PORT": true,
        "NODE_ENV": true,

        // Pattern-specific approvals
        "curl_localhost": true,
        "exact_PORT_8080_node_app_js": true,

        // Dynamically learned commands
        "pytest": true,  // Added during runtime
        "docker": true   // Added during runtime
      }
    }
  }
}
```

## Usage Examples

### Creating a Learning Agent
```bash
# Create agent with learning capabilities
./setup_claude_agent.sh /path/to/project my-agent

# Start the agent
~/.claude-env-my-agent.sh
```

### Real-time Monitoring
```bash
# Monitor all agents (check every 3 seconds)
./approval_monitor.py --interval 3

# List learned commands for specific agent
./approval_monitor.py --list-commands my-agent

# Run as background daemon
./approval_monitor.py --daemon
```

### Programmatic Usage
```python
from claude_agent_manager import ClaudeAgentManager

manager = ClaudeAgentManager()

# Create learning agent
session = manager.create_project_session("/path/to/project", "my-session")

# Monitor and learn from approvals
manager.auto_approve_all_agents()
```

## Learning Algorithm

### 1. Dialog Detection
```python
approval_patterns = [
    "Do you want to proceed?",
    "❯ 1. Yes",
    "2. Yes, and don't ask again",
    "3. No, and tell Claude what to do differently"
]
```

### 2. Command Extraction
```python
# Multiple regex patterns for different command types
patterns = [
    r'Bash command\s*│\s*│\s*│\s*([^\n]+)',  # Direct bash commands
    r'(curl\s+[^\n│]+)',                      # Curl commands
    r'(PORT=\d+\s+[^\n│]+)',                  # Environment variables
    # ... additional patterns
]
```

### 3. Configuration Update
```python
# Add to approved list with different granularities
project_config['autoApproveCommands'] = {
    base_command: True,           # e.g., "curl": true
    env_variable: True,           # e.g., "PORT": true
    exact_pattern: True,          # e.g., "exact_curl_localhost_3000": true
    host_pattern: True            # e.g., "curl_localhost": true
}
```

## Benefits

### 🚀 Progressive Autonomy
- Agents become more autonomous with each approval
- Reduces human intervention over time
- Learns project-specific command patterns

### 📈 Efficiency Gains
- Eliminates repetitive approval dialogs
- Faster development workflows
- Reduced context switching for developers

### 🔒 Controlled Learning
- Only learns from explicitly approved commands
- Maintains security through human oversight
- Project-specific approval scopes

### 🔄 Persistent Knowledge
- Learned approvals persist across sessions
- Shareable configurations between agents
- Transferable learning between similar projects

## Advanced Features

### Multi-Agent Learning
- Each agent maintains its own learned command set
- Configurations can be shared between similar projects
- Global patterns can be extracted and reused

### Pattern Recognition
- Intelligent detection of command families
- Environment variable pattern matching
- URL and path pattern recognition

### Safety Mechanisms
- Only approved commands are learned
- Project-scoped approval lists
- Human oversight maintained for security-sensitive operations

## Monitoring and Debugging

### Log Files
- `logs/approval_monitor.log`: Real-time monitoring logs
- `logs/orchestrator.log`: General orchestrator logs

### Configuration Inspection
```bash
# View current approved commands
grep -A20 "autoApproveCommands" ~/.claude-agent-SESSIONNAME.json

# Monitor learning in real-time
tail -f logs/approval_monitor.log
```

### Statistics Tracking
- Total approvals processed
- Commands learned per session
- Sessions monitored
- Learning rate metrics

## Future Enhancements

### Planned Features
- **Shared Learning**: Agents learn from each other's approvals
- **Pattern Templates**: Pre-built approval patterns for common frameworks
- **Smart Suggestions**: Recommend approvals based on project type
- **Risk Assessment**: Automatic risk scoring for command approvals
- **Learning Analytics**: Dashboard for learning metrics and patterns

This self-learning system transforms Claude agents from reactive approval-seekers into proactive, autonomous development partners that continuously improve their operational efficiency.