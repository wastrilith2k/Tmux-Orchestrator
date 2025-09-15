#!/usr/bin/env python3
"""
Automated Hub Orchestrator - Continuous Agent Management Service

This service runs continuously to:
- Assign agents to pending projects automatically
- Monitor agent health and detect stuck states
- Send automated guidance to stuck agents
- Ensure projects progress autonomously
- Log all orchestration activities

Runs every 30 seconds to maintain autonomous operation.
"""

import asyncio
import requests
import subprocess
import json
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os
import sys

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class HubOrchestrator:
    def __init__(self, api_base_url: str = "http://localhost:8080"):
        self.api_base_url = api_base_url
        self.check_interval = 30  # seconds
        self.stuck_threshold = 300  # 5 minutes without activity = stuck
        self.max_retry_attempts = 3

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('/tmp/hub-orchestrator.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('HubOrchestrator')

    def run_continuous_orchestration(self):
        """Main orchestration loop - runs every 30 seconds"""
        self.logger.info("🚀 Starting Hub Orchestrator - Autonomous Agent Management")

        try:
            while True:
                self.logger.info("🔄 Starting orchestration cycle...")

                # Assign agents to pending projects
                self.assign_agents_to_pending_projects()

                # Monitor and maintain existing agents
                self.monitor_agent_health()

                self.logger.info("✅ Orchestration cycle completed")
                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            self.logger.info("🛑 Orchestrator stopped by user")
        except Exception as e:
            self.logger.error(f"❌ Orchestration error: {e}")
            time.sleep(10)  # Wait before retrying

    def monitor_agent_health(self):
        """Monitor running agents and restart stuck ones"""
        try:
            # Get all running projects
            resp = requests.get(f"{self.api_base_url}/api/projects")
            if resp.status_code != 200:
                return

            projects = resp.json()
            running_projects = [p for p in projects if p['status'] in ['starting', 'running']]

            for project in running_projects:
                session_name = f"proj-{project['name'].lower().replace(' ', '-')}"

                # Check if tmux session exists
                result = subprocess.run(['tmux', 'has-session', '-t', session_name],
                                      capture_output=True, text=True)

                if result.returncode != 0:
                    self.logger.warning(f"🔄 Session {session_name} missing, recreating...")
                    # Reset to pending to recreate
                    requests.put(f"{self.api_base_url}/api/projects/{project['id']}",
                               json={"status": "pending"})
                    continue

                # Check if agent is active (has recent activity)
                try:
                    activity_check = subprocess.run([
                        'tmux', 'capture-pane', '-t', f'{session_name}:0', '-p'
                    ], capture_output=True, text=True, timeout=5)

                    if activity_check.returncode == 0:
                        output = activity_check.stdout

                        # Check for signs of stuck agent
                        if ("login" in output.lower() or
                            "authentication" in output.lower() or
                            "error" in output.lower() and "failed" in output.lower()):

                            self.logger.warning(f"🚨 Agent {session_name} appears stuck, restarting...")
                            self.restart_stuck_agent(session_name, project)
                        else:
                            # Agent seems healthy, update status to running
                            if project['status'] == 'starting':
                                requests.put(f"{self.api_base_url}/api/projects/{project['id']}",
                                           json={"status": "running"})
                                self.logger.info(f"✅ Agent {session_name} confirmed running")

                except Exception as e:
                    self.logger.debug(f"Could not check agent {session_name}: {e}")

        except Exception as e:
            self.logger.error(f"Error monitoring agent health: {e}")

    def restart_stuck_agent(self, session_name: str, project: Dict):
        """Restart a stuck agent"""
        try:
            # Kill the stuck session
            subprocess.run(['tmux', 'kill-session', '-t', session_name],
                         capture_output=True, text=True)

            # Reset project to pending for recreation
            requests.put(f"{self.api_base_url}/api/projects/{project['id']}",
                       json={"status": "pending"})

            self.logger.info(f"🔄 Restarted stuck agent for {project['name']}")

        except Exception as e:
            self.logger.error(f"Failed to restart agent {session_name}: {e}")

    def deploy_project_managers(self):
        """Deploy Project Manager agents for projects that don't have them"""
        try:
            projects = self.get_projects()

            for project in projects:
                if project['status'] in ['running', 'managed']:
                    session_name = f"proj-{project['name'].lower().replace(' ', '-')}"
                    pm_session_name = f"pm-{project['name'].lower().replace(' ', '-')}"

                    # Check if PM already exists
                    pm_check = subprocess.run(['tmux', 'has-session', '-t', pm_session_name],
                                            capture_output=True, text=True)

                    if pm_check.returncode != 0:  # PM doesn't exist
                        project_path = f"/home/james/test-projects/{project['name'].lower().replace(' ', '-')}"

                        if os.path.exists(project_path):
                            self.logger.info(f"🎯 Deploying Project Manager for {project['name']}")

                            # Create PM session
                            pm_create = subprocess.run([
                                'tmux', 'new-session', '-d', '-s', pm_session_name,
                                '-c', project_path,
                                f"/home/james/projs/Tmux-Orchestrator/project_manager_agent.sh {project['name']} {project_path} {session_name}"
                            ], capture_output=True, text=True)

                            if pm_create.returncode == 0:
                                self.logger.info(f"✅ Project Manager deployed for {project['name']}")

                                # Update project status to managed
                                requests.put(f"{self.api_base_url}/api/projects/{project['id']}",
                                           json={"status": "managed"})
                            else:
                                self.logger.error(f"❌ Failed to deploy PM for {project['name']}: {pm_create.stderr}")

        except Exception as e:
            self.logger.error(f"Error deploying project managers: {e}")

    def monitor_project_manager_health(self):
        """Monitor health of Project Manager agents"""
        try:
            # Get all sessions starting with 'pm-'
            sessions_result = subprocess.run(['tmux', 'list-sessions', '-F', '#{session_name}'],
                                           capture_output=True, text=True)

            if sessions_result.returncode == 0:
                all_sessions = sessions_result.stdout.strip().split('\n') if sessions_result.stdout.strip() else []
                pm_sessions = [s for s in all_sessions if s.startswith('pm-')]

                for session_name in pm_sessions:
                    # Check PM activity
                    activity_check = subprocess.run([
                        'tmux', 'capture-pane', '-t', session_name, '-p'
                    ], capture_output=True, text=True)

                    if activity_check.returncode == 0:
                        output = activity_check.stdout
                        if "PROJECT_MANAGER" in output and "CYCLE" in output:
                            self.logger.debug(f"✅ PM {session_name} is active")
                        else:
                            self.logger.warning(f"⚠️ PM {session_name} may be inactive")

        except Exception as e:
            self.logger.error(f"Error monitoring project manager health: {e}")

    def orchestration_cycle(self):
        """Single orchestration cycle - check and manage all projects/agents"""
        self.logger.info("🔄 Starting orchestration cycle...")

        # 1. Check for pending projects and assign agents
        self.assign_agents_to_pending_projects()

        # 2. Deploy Project Managers for active projects
        self.deploy_project_managers()

        # 3. Enable auto-approval for all active sessions
        self.enable_auto_approval_for_all_sessions()

        # 4. Monitor existing agents for stuck states
        self.monitor_agent_health()

        # 5. Monitor Project Manager health
        self.monitor_project_manager_health()

        # 6. Update system metrics
        self.update_system_health()

        self.logger.info("✅ Orchestration cycle completed")

    def assign_agents_to_pending_projects(self):
        """Auto-assign agents to projects with 'pending' status"""
        try:
            # Get all pending projects
            resp = requests.get(f"{self.api_base_url}/api/projects")
            if resp.status_code != 200:
                self.logger.error(f"Failed to get projects: {resp.status_code}")
                return

            projects = resp.json()
            pending_projects = [p for p in projects if p['status'] == 'pending']

            if not pending_projects:
                self.logger.debug("No pending projects found")
                return

            self.logger.info(f"📋 Found {len(pending_projects)} pending projects")

            for project in pending_projects:
                self.create_and_assign_agent(project)

        except Exception as e:
            self.logger.error(f"Error assigning agents to pending projects: {e}")

    def create_and_assign_agent(self, project: Dict):
        """Create an agent and assign it to a project"""
        project_name = project['name']
        project_id = project['id']
        project_type = project['project_type']
        project_path = project['project_path']

        self.logger.info(f"🤖 Creating agent for project: {project_name}")

        try:
            # Create tmux session for the project
            session_name = f"proj-{project_name.lower().replace(' ', '-')}"

            # Check if session already exists
            result = subprocess.run(['tmux', 'has-session', '-t', session_name],
                                  capture_output=True, text=True)

            if result.returncode != 0:
                # Create new tmux session
                subprocess.run([
                    'tmux', 'new-session', '-d', '-s', session_name,
                    '-c', project_path
                ], check=True)

                self.logger.info(f"📺 Created tmux session: {session_name}")

                # Create autonomous development agent script
                self.create_autonomous_agent_script(session_name, project)

                # Start the autonomous agent
                subprocess.run([
                    'tmux', 'send-keys', '-t', f'{session_name}:0',
                    f'bash autonomous_agent_{session_name.replace("-", "_")}.sh', 'Enter'
                ], cwd=project_path, check=True)

                self.logger.info(f"🤖 Started autonomous agent in {session_name}")

                # Wait a moment for agent to start
                time.sleep(2)

            # Update project status to 'starting'
            resp = requests.put(
                f"{self.api_base_url}/api/projects/{project_id}",
                json={"status": "starting"}
            )
            if resp.status_code == 200:
                self.logger.info(f"✅ Project {project_name} status updated to 'starting'")
            else:
                self.logger.error(f"Failed to update project status: {resp.status_code}")

        except Exception as e:
            self.logger.error(f"Failed to create agent for {project_name}: {e}")

    def create_autonomous_agent_script(self, session_name: str, project: Dict):
        """Create an autonomous development agent script"""
        project_path = project['project_path']
        project_type = project['project_type']
        project_name = project['name']

        script_name = f"autonomous_agent_{session_name.replace('-', '_')}.sh"
        script_path = os.path.join(project_path, script_name)

        # Create simple autonomous script
        script_lines = [
            "#!/bin/bash",
            f"# Autonomous Development Agent for {project_name}",
            "set -e",
            "",
            f'PROJECT_PATH="{project_path}"',
            f'PROJECT_TYPE="{project_type}"',
            f'SESSION_NAME="{session_name}"',
            'ORCHESTRATOR_PATH="/home/james/projs/Tmux-Orchestrator"',
            "",
            'cd "$PROJECT_PATH"',
            f'echo "🤖 Autonomous Agent Starting for {project_name}"',
            'echo "📁 Working in: $(pwd)"',
            "",
            "# Initialize git if needed",
            'if [ ! -d ".git" ]; then',
            '    echo "🔧 Initializing git repository..."',
            '    git init',
            '    git add .',
            f'    git commit -m "Initial commit: {project_name} setup"',
            'fi',
            "",
            "# Function to commit progress",
            'commit_progress() {',
            '    local message="$1"',
            '    git add -A',
            '    if git diff --cached --quiet; then',
            '        echo "📝 No changes to commit"',
            '    else',
            '        git commit -m "Progress: $message - $(date)"',
            '        echo "✅ Committed: $message"',
            '    fi',
            '}',
            "",
            "# Setup development environment",
            'if [ "$PROJECT_TYPE" = "python" ]; then',
            '    if [ -f "requirements.txt" ]; then',
            '        echo "📦 Installing Python dependencies..."',
            '        if [ ! -d "venv" ]; then python3 -m venv venv; fi',
            '        if [ -f "venv/bin/activate" ]; then',
            '            source venv/bin/activate',
            '            pip install -r requirements.txt',
            '            commit_progress "Install Python dependencies"',
            '        else',
            '            echo "⚠️  Virtual environment creation failed, installing globally"',
            '            pip3 install -r requirements.txt',
            '            commit_progress "Install Python dependencies (global)"',
            '        fi',
            '    fi',
            'elif [ "$PROJECT_TYPE" = "nodejs" ]; then',
            '    if [ -f "package.json" ]; then',
            '        echo "📦 Installing Node.js dependencies..."',
            '        npm install',
            '        commit_progress "Install Node.js dependencies"',
            '    fi',
            'fi',
            "",
            "# Create README if missing",
            'if [ ! -f "README.md" ]; then',
            '    cat > README.md << EOF',
            f'# {project_name}',
            '',
            f'Project Type: {project_type}',
            'Status: 🤖 Managed by autonomous agent',
            '',
            'EOF',
            '    commit_progress "Create README.md"',
            'fi',
            "",
            "# Work continuously",
            'cycle=0',
            'while true; do',
            '    cycle=$((cycle + 1))',
            '    echo "🔄 Work cycle #$cycle - $(date)"',
            '    ',
            '    # Commit every 30 cycles (30 minutes)',
            '    if [ $((cycle % 60)) -eq 0 ]; then',
            '        commit_progress "Cycle #$cycle autonomous development"',
            '    fi',
            '    ',
            '    # Update activity log',
            '    echo "$(date): Cycle #$cycle completed" >> .agent_activity.log',
            '    ',
            '    sleep 30',
            'done'
        ]

        # Write the script
        with open(script_path, 'w') as f:
            f.write('\n'.join(script_lines))

        # Make it executable
        os.chmod(script_path, 0o755)

        self.logger.info(f"📝 Created autonomous agent script: {script_path}")

    def send_agent_briefing(self, session_name: str, project: Dict):
        """Send initial briefing to a newly created agent"""
        briefing = f"""🎯 AUTONOMOUS DEVELOPMENT ASSIGNMENT

Project: {project['name']}
Type: {project['project_type']}
Path: {project['project_path']}
Description: {project.get('description', 'No description')}

📋 YOUR MISSION:
1. Analyze the existing project structure in {project['project_path']}
2. Set up the development environment:
   - For Node.js projects: Run 'npm install' if package.json exists
   - For Python projects: Run 'pip install -r requirements.txt' if requirements.txt exists
   - Create virtual environments as needed
3. Start the development server (npm run dev, uvicorn, etc.)
4. Begin implementing features based on the project type
5. Commit progress every 30 minutes with meaningful messages
6. Use ./send-claude-message.sh to report status updates
7. Schedule check-ins with ./schedule_with_note.sh

🤖 AUTONOMOUS OPERATION:
- Work independently without waiting for instructions
- Make reasonable development decisions based on project type
- If stuck for >2 minutes, ask specific questions
- Focus on creating a working, deployable application

⚠️ CRITICAL REQUIREMENTS:
- git commit -am "progress update" every 30 minutes
- Send status updates every hour using ./send-claude-message.sh
- Never wait idle - always be developing or improving

🚀 BEGIN DEVELOPMENT NOW - No further instructions needed!
Type 'cd {project['project_path']} && ls -la' to start."""

        # First, enable auto-approval for the agent
        try:
            # Send option "2" to enable auto-approval if there's a prompt
            result = subprocess.run([
                'tmux', 'send-keys', '-t', f'{session_name}:0', '2', 'Enter'
            ], capture_output=True, text=True, timeout=5)
            time.sleep(1)  # Give it a moment
        except Exception:
            pass  # Ignore if there's no prompt

        # Send briefing using existing messaging script
        try:
            result = subprocess.run([
                './send-claude-message.sh', f'{session_name}:0', briefing
            ], cwd='/home/james/projs/Tmux-Orchestrator', capture_output=True, text=True)

            if result.returncode == 0:
                self.logger.info(f"📨 Sent briefing to agent in {session_name}")
            else:
                self.logger.error(f"Failed to send briefing: {result.stderr}")

        except Exception as e:
            self.logger.error(f"Error sending briefing: {e}")

    def enable_auto_approval(self, session_name: str):
        """Enable auto-approval for an agent by sending option 2"""
        try:
            # Check if there's a session first
            result = subprocess.run([
                'tmux', 'list-sessions', '-F', '#{session_name}'
            ], capture_output=True, text=True)

            if session_name not in result.stdout:
                return False

            # Send option "2" to enable auto-approval
            subprocess.run([
                'tmux', 'send-keys', '-t', f'{session_name}:0', '2', 'Enter'
            ], capture_output=True, text=True, timeout=5)

            self.logger.info(f"🔓 Enabled auto-approval for {session_name}")
            return True

        except Exception as e:
            self.logger.error(f"Error enabling auto-approval for {session_name}: {e}")
            return False

    def enable_auto_approval_for_all_sessions(self):
        """Enable auto-approval for all active tmux sessions ending with -dev"""
        try:
            # Get all tmux sessions
            result = subprocess.run([
                'tmux', 'list-sessions', '-F', '#{session_name}'
            ], capture_output=True, text=True)

            if result.returncode != 0:
                return

            sessions = result.stdout.strip().split('\n')
            dev_sessions = [s for s in sessions if s.endswith('-dev')]

            for session in dev_sessions:
                self.enable_auto_approval(session)

        except Exception as e:
            self.logger.error(f"Error enabling auto-approval for all sessions: {e}")

    def monitor_agent_health(self):
        """Monitor existing agents for stuck states and send guidance"""
        try:
            # Get list of project tmux sessions
            result = subprocess.run(['tmux', 'list-sessions'], capture_output=True, text=True)
            if result.returncode != 0:
                return

            project_sessions = []
            for line in result.stdout.strip().split('\n'):
                if line.startswith('proj-'):
                    session_name = line.split(':')[0]
                    project_sessions.append(session_name)

            for session_name in project_sessions:
                self.check_agent_activity(session_name)

        except Exception as e:
            self.logger.error(f"Error monitoring agent health: {e}")

    def check_agent_activity(self, session_name: str):
        """Check if an agent is stuck and needs guidance"""
        try:
            # Capture recent terminal output
            result = subprocess.run([
                'tmux', 'capture-pane', '-t', f'{session_name}:0', '-p'
            ], capture_output=True, text=True)

            if result.returncode != 0:
                return

            terminal_output = result.stdout

            # Check for signs that agent is stuck
            stuck_indicators = [
                "Do you want to proceed?",
                "❯ 1. Yes",
                "❯ 2. Yes, and don't ask again",
                "❯ 3. No, and tell Claude what to do",
                "Continue?",
                "Press any key to continue",
                "[Y/n]",
                "Waiting for input",
                "Type 'exit' to quit"
            ]

            is_stuck = any(indicator in terminal_output for indicator in stuck_indicators)

            if is_stuck:
                self.logger.warning(f"🚨 Agent {session_name} appears to be stuck!")
                self.unstick_agent(session_name, terminal_output)
            else:
                # Check for productivity - look for recent commits
                self.check_agent_productivity(session_name)

        except Exception as e:
            self.logger.error(f"Error checking agent activity for {session_name}: {e}")

    def unstick_agent(self, session_name: str, terminal_output: str):
        """Send commands to unstick a stuck agent"""
        try:
            self.logger.info(f"🔧 Attempting to unstick agent {session_name}")

            # Common unsticking strategies
            if "Do you want to proceed?" in terminal_output or "❯ 1. Yes" in terminal_output:
                # Send "1" to select "Yes"
                subprocess.run(['tmux', 'send-keys', '-t', f'{session_name}:0', '1', 'Enter'])
                self.logger.info(f"📤 Sent '1' to {session_name} to proceed")

            elif "[Y/n]" in terminal_output or "Continue?" in terminal_output:
                # Send "y" for yes
                subprocess.run(['tmux', 'send-keys', '-t', f'{session_name}:0', 'y', 'Enter'])
                self.logger.info(f"📤 Sent 'y' to {session_name} to continue")

            elif "Press any key to continue" in terminal_output:
                # Send Enter
                subprocess.run(['tmux', 'send-keys', '-t', f'{session_name}:0', 'Enter'])
                self.logger.info(f"📤 Sent Enter to {session_name} to continue")

            # Send motivational message
            motivational_msg = """🔄 UNSTUCK PROTOCOL ACTIVATED

The orchestrator detected you were waiting for input. I've automatically responded to continue your work.

🎯 REFOCUS ON YOUR MISSION:
- Continue developing the project
- Make commits every 30 minutes
- Don't wait for confirmations - be autonomous
- Focus on building working features

⚡ PRODUCTIVITY BOOST: Use these patterns:
- git commit -am "feature: what you built"
- npm install / pip install dependencies immediately
- Start development servers and begin coding
- Ask specific technical questions only when truly blocked

🚀 RESUME AUTONOMOUS DEVELOPMENT NOW!"""

            subprocess.run([
                './send-claude-message.sh', f'{session_name}:0', motivational_msg
            ], cwd='/home/james/projs/Tmux-Orchestrator')

        except Exception as e:
            self.logger.error(f"Error unsticking agent {session_name}: {e}")

    def check_agent_productivity(self, session_name: str):
        """Check if agent is making regular commits and progress"""
        try:
            # This would check git history, file modifications, etc.
            # For now, just send periodic encouragement

            # Send periodic check-in every 10 minutes
            current_time = datetime.now()
            if current_time.minute % 10 == 0:
                encouragement = f"""⏰ PRODUCTIVITY CHECK-IN ({current_time.strftime('%H:%M')})

🎯 Quick Status Reminder:
- Have you made a git commit in the last 30 minutes?
- Are you actively developing features?
- Any blockers that need specific technical help?

💪 Keep up the autonomous development!
Next expected commit: {(current_time + timedelta(minutes=30)).strftime('%H:%M')}

Continue your excellent work! 🚀"""

                subprocess.run([
                    './send-claude-message.sh', f'{session_name}:0', encouragement
                ], cwd='/home/james/projs/Tmux-Orchestrator')

        except Exception as e:
            self.logger.error(f"Error checking productivity for {session_name}: {e}")

    def update_system_health(self):
        """Update system health metrics"""
        try:
            # Count active sessions
            result = subprocess.run(['tmux', 'list-sessions'], capture_output=True, text=True)
            active_sessions = len([line for line in result.stdout.split('\n')
                                 if line.startswith('proj-')]) if result.returncode == 0 else 0

            self.logger.debug(f"📊 Active project sessions: {active_sessions}")

        except Exception as e:
            self.logger.error(f"Error updating system health: {e}")

def main():
    """Main entry point"""
    orchestrator = HubOrchestrator()
    orchestrator.run_continuous_orchestration()

if __name__ == "__main__":
    main()