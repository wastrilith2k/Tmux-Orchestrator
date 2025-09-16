#!/usr/bin/env python3
"""
Containerized Engineer Agent for Tmux Orchestrator
Uses Redis pub/sub for communication instead of direct tmux messaging
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

class ContainerizedEngineerAgent:
    def __init__(self, project_name, project_path):
        self.project_name = project_name
        self.project_path = Path(project_path)
        self.cycle_count = 0
        
        # Redis connection for communication
        redis_url = os.getenv('REDIS_URL', 'redis://redis:6379')
        self.redis_client = redis.from_url(redis_url)
        self.pubsub = self.redis_client.pubsub()
        
        # Subscribe to messages for this agent
        self.channel = f"agent:engineer:{project_name}"
        self.pubsub.subscribe(self.channel)
        
        self.log_activity("🔧 Containerized Engineer Agent initialized")
        
    def log_activity(self, message):
        """Log activity with timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] ENGINEER [{self.project_name}]: {message}"
        print(log_message)
        
        # Also log to file
        log_file = self.project_path / "engineer.log"
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
    
    def check_project_state(self):
        """Analyze current project state"""
        os.chdir(self.project_path)
        
        # Check for common project files
        has_package_json = (self.project_path / "package.json").exists()
        has_requirements = (self.project_path / "requirements.txt").exists()
        has_dockerfile = (self.project_path / "Dockerfile").exists()
        has_readme = (self.project_path / "README.md").exists()
        
        # Check git status
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True)
            files_changed = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
        except:
            files_changed = 0
        
        return {
            'has_package_json': has_package_json,
            'has_requirements': has_requirements,
            'has_dockerfile': has_dockerfile,
            'has_readme': has_readme,
            'files_changed': files_changed
        }
    
    def implement_features(self):
        """Implement features based on project type"""
        project_state = self.check_project_state()
        
        if project_state['has_package_json']:
            self.log_activity("📦 Working on Node.js project")
            self.work_on_nodejs_project()
        elif project_state['has_requirements']:
            self.log_activity("🐍 Working on Python project")
            self.work_on_python_project()
        else:
            self.log_activity("🔍 Analyzing project requirements")
            self.analyze_and_setup_project()
    
    def work_on_nodejs_project(self):
        """Work on Node.js specific tasks"""
        # Check if dependencies are installed
        if not (self.project_path / "node_modules").exists():
            self.log_activity("📥 Installing Node.js dependencies")
            try:
                subprocess.run(['npm', 'install'], cwd=self.project_path, check=True)
                self.log_activity("✅ Dependencies installed successfully")
            except subprocess.CalledProcessError as e:
                self.log_activity(f"❌ Failed to install dependencies: {e}")
        
        # Look for missing essential files
        if not (self.project_path / "server.js").exists() and not (self.project_path / "index.js").exists():
            self.log_activity("🔧 Creating basic server structure")
            # Implementation would go here
    
    def work_on_python_project(self):
        """Work on Python specific tasks"""
        self.log_activity("🐍 Python project development tasks")
        # Python-specific implementation
    
    def analyze_and_setup_project(self):
        """Analyze project and set up basic structure"""
        self.log_activity("🔍 Setting up project structure")
        # Project analysis and setup
    
    def commit_progress(self):
        """Commit current progress to git"""
        try:
            os.chdir(self.project_path)
            
            # Check if there are changes to commit
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True)
            
            if result.stdout.strip():
                # Add all changes
                subprocess.run(['git', 'add', '.'], check=True)
                
                # Commit with descriptive message
                commit_msg = f"Progress: Engineering cycle #{self.cycle_count} - automated development"
                subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
                
                self.log_activity("✅ Progress committed to git")
                
                # Notify PM of commit
                pm_channel = f"agent:pm:{self.project_name}"
                self.send_message(pm_channel, f"📝 Committed changes: cycle #{self.cycle_count}")
            else:
                self.log_activity("ℹ️ No changes to commit")
                
        except subprocess.CalledProcessError as e:
            self.log_activity(f"❌ Git commit failed: {e}")
    
    def process_messages(self):
        """Process incoming messages"""
        try:
            message = self.pubsub.get_message(timeout=0.1)
            if message and message['type'] == 'message':
                data = json.loads(message['data'])
                self.log_activity(f"📨 Received message: {data['message']}")
                
                # Process different message types
                msg_content = data['message'].lower()
                if 'implement' in msg_content or 'develop' in msg_content:
                    self.log_activity("🎯 Received development task")
                elif 'commit' in msg_content:
                    self.log_activity("💾 Received commit request")
                    self.commit_progress()
                elif 'status' in msg_content:
                    state = self.check_project_state()
                    status_msg = f"Status: {state['files_changed']} files changed"
                    pm_channel = f"agent:pm:{self.project_name}"
                    self.send_message(pm_channel, status_msg)
                    
        except Exception as e:
            self.log_activity(f"❌ Error processing messages: {e}")
    
    async def run_cycle(self):
        """Main agent cycle"""
        while True:
            self.cycle_count += 1
            self.log_activity(f"=== ENGINEER CYCLE #{self.cycle_count} ===")
            
            # Process any incoming messages
            self.process_messages()
            
            # Perform engineering work
            self.implement_features()
            
            # Commit progress every few cycles
            if self.cycle_count % 3 == 0:
                self.commit_progress()
            
            # Send status update to PM
            pm_channel = f"agent:pm:{self.project_name}"
            self.send_message(pm_channel, f"Engineering cycle #{self.cycle_count} complete")
            
            self.log_activity(f"Cycle #{self.cycle_count} complete - next in 30 seconds")
            await asyncio.sleep(30)  # Engineer cycles every 30 seconds

def main():
    if len(sys.argv) != 3:
        print("Usage: containerized-engineer-agent.py <project_name> <project_path>")
        sys.exit(1)
    
    project_name = sys.argv[1]
    project_path = sys.argv[2]
    
    agent = ContainerizedEngineerAgent(project_name, project_path)
    
    try:
        asyncio.run(agent.run_cycle())
    except KeyboardInterrupt:
        agent.log_activity("🛑 Agent stopped by user")
    except Exception as e:
        agent.log_activity(f"💥 Agent crashed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()