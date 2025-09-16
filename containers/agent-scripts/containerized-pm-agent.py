#!/usr/bin/env python3
"""
Containerized Project Manager Agent for Tmux Orchestrator
Coordinates team activities via Redis pub/sub communication
"""

import os
import sys
import time
import json
import redis
import asyncio
import subprocess
from datetime import datetime
from pathlib import Path

class ContainerizedProjectManagerAgent:
    def __init__(self, project_name, project_path):
        self.project_name = project_name
        self.project_path = Path(project_path)
        self.cycle_count = 0

        # Redis connection for communication
        redis_url = os.getenv('REDIS_URL', 'redis://redis:6379')
        self.redis_client = redis.from_url(redis_url)
        self.pubsub = self.redis_client.pubsub()

        # Subscribe to messages for this agent
        self.channel = f"agent:pm:{project_name}"
        self.pubsub.subscribe(self.channel)

        # Team channels
        self.engineer_channel = f"agent:engineer:{project_name}"
        self.qa_channel = f"agent:qa-engineer:{project_name}"
        self.devops_channel = f"agent:devops:{project_name}"

        self.log_activity("👔 Containerized Project Manager Agent initialized")

    def log_activity(self, message):
        """Log activity with timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] PROJECT_MANAGER [{self.project_name}]: {message}"
        print(log_message)

        # Also log to file
        log_file = self.project_path / "project_manager.log"
        with open(log_file, 'a') as f:
            f.write(log_message + "\n")

    def send_message(self, target_channel, message):
        """Send message via Redis pub/sub"""
        try:
            self.redis_client.publish(target_channel, json.dumps({
                'from': self.channel,
                'message': message,
                'timestamp': datetime.now().isoformat()
            }))
            self.log_activity(f"📤 Message sent to {target_channel}: {message}")
        except Exception as e:
            self.log_activity(f"❌ Failed to send message: {e}")

    def assess_team_status(self):
        """Assess the status of the development team"""
        os.chdir(self.project_path)

        # Check git status
        try:
            result = subprocess.run(['git', 'status', '--porcelain'],
                                  capture_output=True, text=True)
            files_changed = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
        except:
            files_changed = 0

        # Check recent commits
        try:
            result = subprocess.run(['git', 'log', '--oneline', '-10'],
                                  capture_output=True, text=True)
            recent_commits = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
        except:
            recent_commits = 0

        # Check project files
        has_package_json = (self.project_path / "package.json").exists()
        has_requirements = (self.project_path / "requirements.txt").exists()
        has_readme = (self.project_path / "README.md").exists()
        has_tests = any(self.project_path.glob("test*")) or any(self.project_path.glob("*test*"))

        return {
            'files_changed': files_changed,
            'recent_commits': recent_commits,
            'has_package_json': has_package_json,
            'has_requirements': has_requirements,
            'has_readme': has_readme,
            'has_tests': has_tests
        }

    def coordinate_development(self):
        """Coordinate development activities"""
        status = self.assess_team_status()

        self.log_activity(f"Team Status: Files changed: {status['files_changed']}, Recent commits: {status['recent_commits']}")

        # Coordinate based on project state
        if status['files_changed'] > 5:
            self.log_activity("COORDINATION: Many changes detected, suggesting commit")
            self.send_message(self.engineer_channel, "Consider committing current changes")

        if not status['has_tests']:
            self.log_activity("QUALITY ISSUE: No tests detected")
            self.send_message(self.qa_channel, "QA ALERT: No test files found - please create test suite")

        if status['recent_commits'] < 2:
            self.log_activity("PRODUCTIVITY: Low commit activity")
            self.send_message(self.engineer_channel, "PM GUIDANCE: Consider more frequent commits to track progress")

        # Check if deployment is needed
        if status['recent_commits'] > 0:
            self.send_message(self.devops_channel, f"DEPLOYMENT: {status['recent_commits']} new commits ready for deployment")

    def process_team_messages(self):
        """Process incoming messages from team"""
        try:
            message = self.pubsub.get_message(timeout=0.1)
            if message and message['type'] == 'message':
                data = json.loads(message['data'])
                self.log_activity(f"📨 Team Update: {data['message']}")

                # Process different message types
                msg_content = data['message'].lower()
                if 'commit' in msg_content:
                    self.log_activity("✅ Team committed changes")
                elif 'error' in msg_content or 'failed' in msg_content:
                    self.log_activity("⚠️ Team reported issues - investigating")
                    self.send_message(self.engineer_channel, "PM SUPPORT: Issues detected, need assistance?")
                elif 'complete' in msg_content:
                    self.log_activity("🎯 Task completion reported")

        except Exception as e:
            self.log_activity(f"❌ Error processing team messages: {e}")

    def report_to_orchestrator(self):
        """Report project status to orchestrator"""
        status = self.assess_team_status()

        report = {
            'project': self.project_name,
            'pm_cycle': self.cycle_count,
            'status': status,
            'timestamp': datetime.now().isoformat()
        }

        # Send report to orchestrator via Redis
        self.redis_client.setex(
            f"project_status:{self.project_name}",
            300,  # 5 minutes TTL
            json.dumps(report)
        )

        self.log_activity("📊 Project status reported to orchestrator")

    async def run_cycle(self):
        """Main PM cycle"""
        while True:
            self.cycle_count += 1
            self.log_activity(f"=== PROJECT MANAGER CYCLE #{self.cycle_count} ===")

            # Process team messages
            self.process_team_messages()

            # Coordinate development
            self.coordinate_development()

            # Report to orchestrator
            self.report_to_orchestrator()

            self.log_activity(f"Cycle #{self.cycle_count} complete - next in 60 seconds")
            await asyncio.sleep(60)  # PM cycles every minute

def main():
    if len(sys.argv) != 3:
        print("Usage: containerized-pm-agent.py <project_name> <project_path>")
        sys.exit(1)

    project_name = sys.argv[1]
    project_path = sys.argv[2]

    agent = ContainerizedProjectManagerAgent(project_name, project_path)

    try:
        asyncio.run(agent.run_cycle())
    except KeyboardInterrupt:
        agent.log_activity("🛑 PM Agent stopped by user")
    except Exception as e:
        agent.log_activity(f"💥 PM Agent crashed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()