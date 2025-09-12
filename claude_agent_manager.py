#!/usr/bin/env python3

"""
Enhanced Tmux Orchestrator with Claude Agent Management
Integrates with setup_claude_agent.sh for autonomous agent deployment
"""

import subprocess
import json
import time
import os
import logging
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from tmux_utils import TmuxOrchestrator

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/orchestrator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('ClaudeAgentManager')

class ClaudeAgentManager(TmuxOrchestrator):
    """Enhanced Tmux Orchestrator with Claude agent management capabilities"""

    def __init__(self):
        super().__init__()
        self.agent_configs_dir = Path.home() / "claude-agent-configs"
        self.agent_configs_dir.mkdir(exist_ok=True)

    def create_claude_agent(self, session_name: str, project_path: str,
                          window_name: str = "Claude-Agent",
                          working_dir: Optional[str] = None) -> bool:
        """
        Create a new Claude agent with pre-configured approval settings

        Args:
            session_name: Tmux session name
            project_path: Path to the project directory
            window_name: Name for the tmux window
            working_dir: Working directory (defaults to project_path)

        Returns:
            bool: True if agent created successfully
        """
        try:
            if working_dir is None:
                working_dir = project_path

            # Ensure session exists
            if not self.validate_session_exists(session_name):
                logger.info(f"Creating new tmux session: {session_name}")
                subprocess.run([
                    "tmux", "new-session", "-d", "-s", session_name,
                    "-c", working_dir
                ], check=True)

            # Setup Claude agent configuration
            setup_script = Path(__file__).parent / "setup_claude_agent.sh"
            if not setup_script.exists():
                logger.error(f"Setup script not found: {setup_script}")
                return False

            logger.info(f"Setting up Claude configuration for {session_name}")
            subprocess.run([
                str(setup_script), project_path, session_name
            ], check=True, cwd=Path(__file__).parent)

            # Create tmux window for Claude agent
            logger.info(f"Creating tmux window: {window_name}")
            subprocess.run([
                "tmux", "new-window", "-t", session_name,
                "-n", window_name, "-c", working_dir
            ], check=True)

            # Start Claude with pre-configured settings
            agent_env_script = Path.home() / f".claude-env-{session_name}.sh"

            if agent_env_script.exists():
                logger.info(f"Starting Claude agent with pre-configured approvals")
                subprocess.run([
                    "tmux", "send-keys", "-t", f"{session_name}:{window_name}",
                    f"source {agent_env_script}", "Enter"
                ], check=True)
            else:
                # Fallback to regular Claude startup
                logger.warning("Pre-configured environment not found, starting regular Claude")
                subprocess.run([
                    "tmux", "send-keys", "-t", f"{session_name}:{window_name}",
                    "claude", "Enter"
                ], check=True)

            # Give Claude time to start
            time.sleep(3)

            # Send initial briefing
            self.brief_agent(session_name, window_name, project_path)

            logger.info(f"✅ Claude agent created successfully: {session_name}:{window_name}")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create Claude agent: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error creating agent: {e}")
            return False

    def brief_agent(self, session_name: str, window_name: str, project_path: str):
        """Send initial briefing to the Claude agent"""
        briefing = f"""You are now an autonomous Claude agent operating in tmux session '{session_name}'.

PROJECT CONTEXT:
- Working directory: {project_path}
- Your role: Complete development tasks autonomously
- Communication: Use the provided scripts to coordinate with other agents

IMPORTANT OPERATIONAL GUIDELINES:
1. When approval dialogs appear, ALWAYS select option 2 "Yes, and don't ask again" for autonomous operation
2. Commit your work every 30 minutes: git add -A && git commit -m "Progress: [description]"
3. Use ./send-claude-message.sh to communicate with other agents
4. Schedule check-ins with ./schedule_with_note.sh when needed

CURRENT TASK:
- Analyze the project structure
- Read README.md or documentation to understand requirements
- Begin implementation of assigned features
- Test your work regularly

Start by exploring the project and understanding your objectives."""

        # Send briefing using the communication script
        script_path = Path(__file__).parent / "send-claude-message.sh"
        if script_path.exists():
            subprocess.run([
                str(script_path), f"{session_name}:{window_name}", briefing
            ], cwd=Path(__file__).parent)
        else:
            # Fallback to direct tmux send
            subprocess.run([
                "tmux", "send-keys", "-t", f"{session_name}:{window_name}",
                briefing, "Enter"
            ])

    def create_project_session(self, project_path: str, session_name: Optional[str] = None) -> str:
        """
        Create a complete project session with Claude agent and supporting windows

        Args:
            project_path: Path to the project directory
            session_name: Optional session name (defaults to project basename)

        Returns:
            str: The session name that was created
        """
        if session_name is None:
            session_name = Path(project_path).name

        try:
            # Create main session with Shell window
            logger.info(f"Creating project session: {session_name}")
            subprocess.run([
                "tmux", "new-session", "-d", "-s", session_name,
                "-n", "Shell", "-c", project_path
            ], check=True)

            # Create Claude agent window
            self.create_claude_agent(session_name, project_path)

            # Create additional windows as needed
            self.create_dev_server_window(session_name, project_path)

            logger.info(f"✅ Project session created: {session_name}")
            logger.info(f"   - Shell window for manual commands")
            logger.info(f"   - Claude-Agent window with autonomous operation")
            logger.info(f"   - Dev-Server window for application hosting")

            return session_name

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create project session: {e}")
            raise

    def create_dev_server_window(self, session_name: str, project_path: str):
        """Create a development server window"""
        try:
            subprocess.run([
                "tmux", "new-window", "-t", session_name,
                "-n", "Dev-Server", "-c", project_path
            ], check=True)

            # Auto-detect and start development server if possible
            package_json = Path(project_path) / "package.json"
            if package_json.exists():
                subprocess.run([
                    "tmux", "send-keys", "-t", f"{session_name}:Dev-Server",
                    "# Development server ready. Use 'npm start' or 'npm run dev'", "Enter"
                ])
            else:
                subprocess.run([
                    "tmux", "send-keys", "-t", f"{session_name}:Dev-Server",
                    "# Development server window ready", "Enter"
                ])

        except subprocess.CalledProcessError as e:
            logger.warning(f"Could not create dev server window: {e}")

    def extract_command_from_approval_dialog(self, content: str) -> Optional[str]:
        """Extract the command being approved from the dialog content"""
        import re

        # Look for command patterns in approval dialogs
        # Pattern 1: "curl http://..." or similar bash commands
        bash_command_match = re.search(r'Bash command\s*│\s*│\s*│\s*([^\n]+)', content, re.MULTILINE)
        if bash_command_match:
            return bash_command_match.group(1).strip()

        # Pattern 2: Look for commands in the dialog text
        command_patterns = [
            r'│\s*([a-zA-Z][a-zA-Z0-9_-]*(?:\s+[^\n│]+)?)\s*│',  # Generic command
            r'(\w+\s+[^\n│]+)(?=\s*│.*Test|Description)',  # Command with description
            r'(curl\s+[^\n│]+)',  # Curl commands
            r'(npm\s+[^\n│]+)',   # NPM commands
            r'(node\s+[^\n│]+)',  # Node commands
            r'(PORT=\d+\s+[^\n│]+)',  # Environment variable commands
        ]

        for pattern in command_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                command = match.group(1).strip()
                # Clean up command (remove extra whitespace, pipes, etc.)
                command = re.sub(r'\s+', ' ', command)
                return command

        return None

    def add_command_to_approved_list(self, session_name: str, project_path: str, command: str):
        """Add a command to the agent's approved list for future automatic approval"""
        try:
            config_file = Path.home() / f".claude-agent-{session_name}.json"
            if not config_file.exists():
                logger.warning(f"Agent config file not found: {config_file}")
                return False

            # Load current configuration
            with open(config_file, 'r') as f:
                config = json.load(f)

            # Ensure project configuration exists
            if project_path not in config.get('projects', {}):
                logger.warning(f"Project {project_path} not found in agent config")
                return False

            project_config = config['projects'][project_path]

            # Ensure autoApproveCommands section exists
            if 'autoApproveCommands' not in project_config:
                project_config['autoApproveCommands'] = {}

            # Extract command keyword for approval
            command_parts = command.split()
            if not command_parts:
                return False

            # Handle different command patterns
            if '=' in command_parts[0] and len(command_parts) > 1:
                # Environment variable command like "PORT=8080 node app.js"
                env_var = command_parts[0].split('=')[0]
                base_command = command_parts[1]
                project_config['autoApproveCommands'][env_var] = True
                project_config['autoApproveCommands'][base_command] = True
                logger.info(f"Added environment variable '{env_var}' and command '{base_command}' to approved list")
            else:
                # Regular command
                base_command = command_parts[0]
                project_config['autoApproveCommands'][base_command] = True
                logger.info(f"Added command '{base_command}' to approved list")

                # If it's a complex command, also approve common patterns
                if len(command_parts) > 1:
                    # For commands like "curl http://localhost:3000/status", approve "curl" + hostname pattern
                    if base_command == 'curl' and 'localhost' in command:
                        project_config['autoApproveCommands']['curl_localhost'] = True
                        logger.info(f"Added 'curl_localhost' pattern to approved list")

            # Add the full command pattern for exact matches
            command_key = f"exact_{command.replace(' ', '_').replace('/', '_').replace(':', '_')}"
            project_config['autoApproveCommands'][command_key] = True

            # Save updated configuration
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)

            logger.info(f"✅ Updated agent configuration with new approved command: {command}")
            return True

        except Exception as e:
            logger.error(f"Failed to add command to approved list: {e}")
            return False

    def monitor_agent_approvals(self, session_name: str, window_name: str = "Claude-Agent") -> bool:
        """
        Monitor Claude agent for approval dialogs, auto-approve them, and learn from approvals

        Returns:
            bool: True if monitoring is active, False if agent not found
        """
        try:
            # Capture current window content
            content = self.capture_window_content(session_name, window_name, 50)

            # Check for approval dialog patterns
            approval_patterns = [
                "Do you want to proceed?",
                "❯ 1. Yes",
                "2. Yes, and don't ask again",
                "3. No, and tell Claude what to do differently"
            ]

            if all(pattern in content for pattern in approval_patterns[:2]):
                logger.info(f"🔧 Approval dialog detected in {session_name}:{window_name}")

                # Extract the command being approved
                command = self.extract_command_from_approval_dialog(content)
                if command:
                    logger.info(f"📝 Command to approve: {command}")

                    # Get project path for this session
                    project_path = self.get_session_project_path(session_name)
                    if project_path:
                        # Add command to approved list for future automatic approval
                        self.add_command_to_approved_list(session_name, project_path, command)

                # Send option 2 to approve and disable future dialogs
                subprocess.run([
                    "tmux", "send-keys", "-t", f"{session_name}:{window_name}",
                    "2", "Enter"
                ], check=True)

                logger.info("✅ Auto-approved with 'don't ask again' option")
                return True

            return False

        except Exception as e:
            logger.warning(f"Error monitoring approvals: {e}")
            return False

    def get_session_project_path(self, session_name: str) -> Optional[str]:
        """Get the project path associated with a session"""
        try:
            # Try to get working directory from the session
            result = subprocess.run([
                "tmux", "display-message", "-t", session_name, "-p", "#{pane_current_path}"
            ], capture_output=True, text=True)

            if result.returncode == 0:
                return result.stdout.strip()

            # Fallback: check if session name matches a known project
            common_project_paths = [
                f"/home/james/{session_name}",
                f"/home/james/projs/{session_name}",
                f"/home/james/test-{session_name}",
                f"/home/james/test-simple-project"  # For our test case
            ]

            for path in common_project_paths:
                if Path(path).exists():
                    return path

            return None

        except Exception as e:
            logger.warning(f"Could not determine project path for session {session_name}: {e}")
            return None

    def auto_approve_all_agents(self):
        """Monitor all Claude agents and auto-approve any pending dialogs"""
        sessions = self.get_tmux_sessions()
        approved_count = 0

        for session in sessions:
            for window in session.windows:
                if "claude" in window.window_name.lower() or "agent" in window.window_name.lower():
                    if self.monitor_agent_approvals(session.name, window.window_name):
                        approved_count += 1

        if approved_count > 0:
            logger.info(f"Auto-approved {approved_count} pending dialogs")

        return approved_count

def main():
    """Example usage and testing"""
    agent_manager = ClaudeAgentManager()

    # Example: Create a new project session
    test_project = "/home/james/test-simple-project"
    if Path(test_project).exists():
        session_name = agent_manager.create_project_session(test_project, "auto-test")
        print(f"Created session: {session_name}")

        # Monitor for approval dialogs
        time.sleep(5)
        agent_manager.auto_approve_all_agents()

if __name__ == "__main__":
    main()