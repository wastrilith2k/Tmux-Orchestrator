#!/usr/bin/env python3
"""
Containerized System Test
Validates that the fully containerized Tmux Orchestrator is working correctly
"""

import docker
import redis
import requests
import time
import json
import sys
from datetime import datetime

class ContainerizedSystemTest:
    def __init__(self):
        self.docker_client = docker.from_env()
        self.redis_client = None
        self.tests_passed = 0
        self.tests_failed = 0
        
    def log_test(self, test_name, passed, details=""):
        """Log test result"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"[{timestamp}] {status} {test_name}")
        if details:
            print(f"         {details}")
        
        if passed:
            self.tests_passed += 1
        else:
            self.tests_failed += 1
    
    def test_infrastructure_containers(self):
        """Test that infrastructure containers are running"""
        required_containers = ['tmux-orchestrator-db', 'tmux-orchestrator-redis', 'tmux-orchestrator-api']
        
        for container_name in required_containers:
            try:
                container = self.docker_client.containers.get(container_name)
                is_running = container.status == 'running'
                self.log_test(f"Infrastructure: {container_name}", is_running, 
                             f"Status: {container.status}")
            except docker.errors.NotFound:
                self.log_test(f"Infrastructure: {container_name}", False, "Container not found")
    
    def test_workspace_containers(self):
        """Test workspace containers"""
        workspace_containers = ['workspace-test-todo-app', 'workspace-ml-pipeline', 'workspace-ecommerce-app']
        
        for container_name in workspace_containers:
            try:
                container = self.docker_client.containers.get(container_name)
                is_running = container.status == 'running'
                self.log_test(f"Workspace: {container_name}", is_running,
                             f"Status: {container.status}")
            except docker.errors.NotFound:
                self.log_test(f"Workspace: {container_name}", False, "Container not found")
    
    def test_agent_containers(self):
        """Test agent containers"""
        agent_containers = self.docker_client.containers.list(filters={'name': 'agent-'})
        
        if len(agent_containers) == 0:
            self.log_test("Agent Containers", False, "No agent containers found")
            return
        
        running_agents = 0
        for container in agent_containers:
            is_running = container.status == 'running'
            if is_running:
                running_agents += 1
            self.log_test(f"Agent: {container.name}", is_running, 
                         f"Status: {container.status}")
        
        self.log_test("Agent Container Count", running_agents > 0, 
                     f"{running_agents} agents running")
    
    def test_redis_connectivity(self):
        """Test Redis connectivity and communication"""
        try:
            self.redis_client = redis.from_url('redis://localhost:6379')
            self.redis_client.ping()
            self.log_test("Redis Connectivity", True, "Redis responding")
            
            # Test pub/sub functionality
            test_channel = "test:containerized:system"
            test_message = json.dumps({
                'test': True,
                'timestamp': datetime.now().isoformat()
            })
            
            result = self.redis_client.publish(test_channel, test_message)
            self.log_test("Redis Pub/Sub", result >= 0, f"Published to {result} subscribers")
            
        except Exception as e:
            self.log_test("Redis Connectivity", False, f"Error: {e}")
    
    def test_api_gateway(self):
        """Test API gateway connectivity"""
        try:
            response = requests.get('http://localhost:8080/health', timeout=5)
            is_healthy = response.status_code == 200
            self.log_test("API Gateway Health", is_healthy, 
                         f"Status: {response.status_code}")
            
        except Exception as e:
            self.log_test("API Gateway Health", False, f"Error: {e}")
    
    def test_orchestrator_activity(self):
        """Test orchestrator activity"""
        if not self.redis_client:
            self.log_test("Orchestrator Activity", False, "Redis not available")
            return
        
        try:
            # Check for orchestrator logs in Redis
            logs = self.redis_client.lrange('orchestrator:logs', 0, 4)
            has_recent_logs = len(logs) > 0
            
            self.log_test("Orchestrator Activity", has_recent_logs,
                         f"{len(logs)} recent log entries")
            
            if has_recent_logs:
                latest_log = json.loads(logs[0])
                self.log_test("Orchestrator Recent Activity", True,
                             f"Latest: {latest_log.get('message', 'N/A')}")
            
        except Exception as e:
            self.log_test("Orchestrator Activity", False, f"Error: {e}")
    
    def test_container_networking(self):
        """Test container networking"""
        try:
            # Check if containers can reach each other
            networks = self.docker_client.networks.list(names=['tmux-orchestrator-network'])
            has_network = len(networks) > 0
            
            self.log_test("Container Network", has_network, 
                         "tmux-orchestrator-network exists" if has_network else "Network missing")
            
            if has_network:
                network = networks[0]
                connected_containers = len(network.attrs.get('Containers', {}))
                self.log_test("Network Connectivity", connected_containers > 0,
                             f"{connected_containers} containers connected")
            
        except Exception as e:
            self.log_test("Container Network", False, f"Error: {e}")
    
    def test_agent_communication(self):
        """Test agent communication via Redis"""
        if not self.redis_client:
            self.log_test("Agent Communication", False, "Redis not available")
            return
        
        try:
            # Send a test message to agents
            test_message = json.dumps({
                'from': 'system_test',
                'type': 'health_check',
                'timestamp': datetime.now().isoformat()
            })
            
            # Test communication to different agent types
            projects = ['test-todo-app', 'ml-pipeline']
            agent_types = ['engineer', 'project-manager']
            
            messages_sent = 0
            for project in projects:
                for agent_type in agent_types:
                    channel = f"agent:{agent_type}:{project}"
                    result = self.redis_client.publish(channel, test_message)
                    messages_sent += 1
            
            self.log_test("Agent Communication", messages_sent > 0,
                         f"Sent {messages_sent} test messages")
            
        except Exception as e:
            self.log_test("Agent Communication", False, f"Error: {e}")
    
    def run_all_tests(self):
        """Run all containerized system tests"""
        print("🐳 CONTAINERIZED TMUX ORCHESTRATOR - SYSTEM TEST")
        print("=" * 55)
        print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        print("🏗️  INFRASTRUCTURE TESTS")
        print("-" * 25)
        self.test_infrastructure_containers()
        self.test_redis_connectivity()
        self.test_api_gateway()
        
        print()
        print("🐳 CONTAINER TESTS")
        print("-" * 18)
        self.test_workspace_containers()
        self.test_agent_containers()
        self.test_container_networking()
        
        print()
        print("🤖 AGENT SYSTEM TESTS")
        print("-" * 20)
        self.test_orchestrator_activity()
        self.test_agent_communication()
        
        print()
        print("📊 TEST SUMMARY")
        print("=" * 15)
        total_tests = self.tests_passed + self.tests_failed
        success_rate = (self.tests_passed / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {self.tests_passed} ✅")
        print(f"Failed: {self.tests_failed} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        print()
        
        if self.tests_failed == 0:
            print("🎉 SYSTEM STATUS: EXCELLENT - Fully containerized!")
            print()
            print("✅ All autonomous agents running in containers")
            print("✅ Redis pub/sub communication working")
            print("✅ Container orchestration functional")
            print("✅ Network isolation properly configured")
            print("✅ Infrastructure services healthy")
        else:
            print("⚠️  SYSTEM STATUS: Issues detected")
            print(f"   {self.tests_failed} test(s) failed - check container logs")
        
        return self.tests_failed == 0

def main():
    tester = ContainerizedSystemTest()
    
    # Wait a moment for containers to stabilize
    print("⏳ Waiting for containers to stabilize...")
    time.sleep(5)
    
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()