#!/usr/bin/env python3
"""
Tmux Orchestrator - Comprehensive System Test Application
Demonstrates the full autonomous multi-agent development system
"""

import requests
import subprocess
import time
import json
from datetime import datetime
from typing import Dict, List

class TmuxOrchestratorTester:
    def __init__(self, api_url="http://localhost:8080"):
        self.api_url = api_url
        self.test_results = []

    def log_test(self, test_name: str, passed: bool, details: str = ""):
        """Log test result"""
        status = "✅ PASS" if passed else "❌ FAIL"
        timestamp = datetime.now().strftime("%H:%M:%S")
        result = {
            "timestamp": timestamp,
            "test": test_name,
            "status": status,
            "passed": passed,
            "details": details
        }
        self.test_results.append(result)
        print(f"[{timestamp}] {status} {test_name}")
        if details:
            print(f"         {details}")

    def test_api_connectivity(self):
        """Test hub API connectivity"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.log_test("API Health Check", True, f"API healthy: {data.get('status')}")
                return True
            else:
                self.log_test("API Health Check", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("API Health Check", False, f"Connection error: {e}")
            return False

    def test_projects_endpoint(self):
        """Test projects API endpoints"""
        try:
            response = requests.get(f"{self.api_url}/api/projects", timeout=5)
            if response.status_code == 200:
                projects = response.json()
                project_count = len(projects)
                self.log_test("Projects API", True, f"Found {project_count} projects")

                # Check for our test projects
                project_names = [p.get('name', '') for p in projects]
                expected_projects = ['python-ml-pipeline', 'node-ecommerce-app']

                for expected in expected_projects:
                    if expected in project_names:
                        self.log_test(f"Project: {expected}", True, "Project found in API")
                    else:
                        self.log_test(f"Project: {expected}", False, "Project missing from API")

                return True
            else:
                self.log_test("Projects API", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Projects API", False, f"Error: {e}")
            return False

    def test_tmux_sessions(self):
        """Test tmux session availability"""
        try:
            # Get all sessions
            result = subprocess.run(['tmux', 'list-sessions', '-F', '#{session_name}'],
                                  capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                sessions = result.stdout.strip().split('\n') if result.stdout.strip() else []

                # Expected session patterns
                expected_patterns = [
                    ('proj-', 'Engineer Agents'),
                    ('pm-', 'Project Manager Agents'),
                    ('qa-', 'QA Engineer Agents'),
                    ('devops-', 'DevOps Agents')
                ]

                for pattern, description in expected_patterns:
                    matching_sessions = [s for s in sessions if s.startswith(pattern)]
                    count = len(matching_sessions)

                    if count > 0:
                        self.log_test(f"Tmux Sessions: {description}", True,
                                    f"{count} sessions: {', '.join(matching_sessions)}")
                    else:
                        self.log_test(f"Tmux Sessions: {description}", False,
                                    f"No sessions found with pattern '{pattern}'")

                return len(sessions) > 0
            else:
                self.log_test("Tmux Sessions", False, "Could not list tmux sessions")
                return False

        except Exception as e:
            self.log_test("Tmux Sessions", False, f"Error: {e}")
            return False

    def test_agent_activity(self):
        """Test agent activity and communication"""
        try:
            # Test engineer agent activity
            result = subprocess.run(['tmux', 'capture-pane', '-t', 'proj-python-ml-pipeline:0', '-p'],
                                  capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                output = result.stdout
                if "Agent working autonomously" in output or "cycle" in output.lower():
                    self.log_test("Engineer Agent Activity", True, "Agent showing autonomous activity")
                else:
                    self.log_test("Engineer Agent Activity", False, "No autonomous activity detected")
            else:
                self.log_test("Engineer Agent Activity", False, "Could not capture agent output")

            # Test project manager activity
            result = subprocess.run(['tmux', 'capture-pane', '-t', 'pm-python-ml-pipeline:0', '-p'],
                                  capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                output = result.stdout
                if "PROJECT_MANAGER" in output and "CYCLE" in output:
                    self.log_test("Project Manager Activity", True, "PM showing coordination activity")
                else:
                    self.log_test("Project Manager Activity", False, "No PM activity detected")
            else:
                self.log_test("Project Manager Activity", False, "Could not capture PM output")

        except Exception as e:
            self.log_test("Agent Activity", False, f"Error: {e}")

    def test_communication_logs(self):
        """Test agent communication system"""
        try:
            import os
            log_dir = "/home/james/projs/Tmux-Orchestrator/logs/communications"

            if os.path.exists(log_dir):
                today_log = f"{log_dir}/messages-{datetime.now().strftime('%Y%m%d')}.log"

                if os.path.exists(today_log):
                    with open(today_log, 'r') as f:
                        log_content = f.read()

                    # Check for communication patterns
                    success_messages = log_content.count("SUCCESS: Message sent")
                    error_messages = log_content.count("ERROR:")

                    if success_messages > 0:
                        self.log_test("Communication Logs", True,
                                    f"{success_messages} successful messages, {error_messages} errors")
                    else:
                        self.log_test("Communication Logs", False, "No successful messages found")
                else:
                    self.log_test("Communication Logs", False, f"No log file for today: {today_log}")
            else:
                self.log_test("Communication Logs", False, f"Log directory not found: {log_dir}")

        except Exception as e:
            self.log_test("Communication Logs", False, f"Error: {e}")

    def test_git_repositories(self):
        """Test project git repositories"""
        projects = [
            "/home/james/test-projects/ml-pipeline",
            "/home/james/test-projects/ecommerce-app"
        ]

        for project_path in projects:
            project_name = project_path.split('/')[-1]
            try:
                # Check if git repo exists
                result = subprocess.run(['git', 'status'], cwd=project_path,
                                      capture_output=True, text=True, timeout=10)

                if result.returncode == 0:
                    # Check for commits
                    result = subprocess.run(['git', 'log', '--oneline', '-5'], cwd=project_path,
                                          capture_output=True, text=True, timeout=10)

                    if result.returncode == 0:
                        commit_count = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
                        self.log_test(f"Git Repository: {project_name}", True,
                                    f"{commit_count} recent commits")
                    else:
                        self.log_test(f"Git Repository: {project_name}", False, "No commits found")
                else:
                    self.log_test(f"Git Repository: {project_name}", False, "Not a git repository")

            except Exception as e:
                self.log_test(f"Git Repository: {project_name}", False, f"Error: {e}")

    def create_test_project(self):
        """Create a test project through the API"""
        test_project = {
            "name": "test-autonomous-app",
            "description": "Test project created by autonomous system tester",
            "project_type": "python",
            "project_path": "/home/james/test-projects/test-autonomous-app"
        }

        try:
            response = requests.post(f"{self.api_url}/api/projects",
                                   json=test_project, timeout=10)

            if response.status_code in [200, 201]:
                project_data = response.json()
                project_id = project_data.get('id')
                self.log_test("Create Test Project", True,
                            f"Project created with ID: {project_id}")
                return project_id
            else:
                self.log_test("Create Test Project", False,
                            f"HTTP {response.status_code}: {response.text}")
                return None

        except Exception as e:
            self.log_test("Create Test Project", False, f"Error: {e}")
            return None

    def run_full_test_suite(self):
        """Run complete test suite"""
        print("🚀 TMUX ORCHESTRATOR - COMPREHENSIVE SYSTEM TEST")
        print("=" * 55)
        print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # Core infrastructure tests
        print("📡 INFRASTRUCTURE TESTS")
        print("-" * 25)
        api_healthy = self.test_api_connectivity()
        self.test_projects_endpoint()
        print()

        # Agent system tests
        print("🤖 AGENT SYSTEM TESTS")
        print("-" * 20)
        self.test_tmux_sessions()
        self.test_agent_activity()
        print()

        # Communication tests
        print("📡 COMMUNICATION TESTS")
        print("-" * 21)
        self.test_communication_logs()
        print()

        # Project tests
        print("📁 PROJECT TESTS")
        print("-" * 15)
        self.test_git_repositories()
        print()

        # Integration tests
        print("🔗 INTEGRATION TESTS")
        print("-" * 19)
        if api_healthy:
            self.create_test_project()
        print()

        # Test summary
        self.print_test_summary()

    def print_test_summary(self):
        """Print comprehensive test summary"""
        print("📊 TEST SUMMARY")
        print("=" * 15)

        passed_tests = [r for r in self.test_results if r['passed']]
        failed_tests = [r for r in self.test_results if not r['passed']]

        total_tests = len(self.test_results)
        passed_count = len(passed_tests)
        failed_count = len(failed_tests)
        success_rate = (passed_count / total_tests * 100) if total_tests > 0 else 0

        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_count} ✅")
        print(f"Failed: {failed_count} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        print()

        if failed_count > 0:
            print("❌ FAILED TESTS:")
            for test in failed_tests:
                print(f"   • {test['test']}: {test['details']}")
            print()

        if success_rate >= 80:
            print("🎉 SYSTEM STATUS: EXCELLENT - Ready for production!")
        elif success_rate >= 60:
            print("✅ SYSTEM STATUS: GOOD - Minor issues to address")
        elif success_rate >= 40:
            print("⚠️ SYSTEM STATUS: NEEDS WORK - Several issues detected")
        else:
            print("🚨 SYSTEM STATUS: CRITICAL - Major issues need resolution")

        return success_rate >= 80

if __name__ == "__main__":
    tester = TmuxOrchestratorTester()
    success = tester.run_full_test_suite()

    # Exit with appropriate code
    exit(0 if success else 1)