#!/usr/bin/env python3
"""
Containerized Agent Orchestrator
Manages multiple agent containers, monitors health, and coordinates work
"""

import os
import sys
import time
import json
import redis
import docker
import asyncio
import logging
from datetime import datetime
from typing import Dict, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ContainerizedOrchestrator:
    def __init__(self):
        # Redis connection for communication
        redis_url = os.getenv('REDIS_URL', 'redis://redis:6379')
        self.redis_client = redis.from_url(redis_url)
        
        # Docker client for container management
        self.docker_client = docker.from_env()
        
        # Hub API URL
        self.hub_api_url = os.getenv('HUB_API_URL', 'http://api-gateway:80')
        
        # Agent tracking
        self.agents = {}
        self.projects = ['test-todo-app', 'ml-pipeline', 'ecommerce-app']
        self.agent_types = ['engineer', 'project-manager', 'qa-engineer', 'devops']
        
        logger.info("🤖 Containerized Orchestrator initialized")
        
    def log_activity(self, message):
        """Log activity with timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] ORCHESTRATOR: {message}"
        logger.info(message)
        
        # Store in Redis for dashboard
        self.redis_client.lpush('orchestrator:logs', json.dumps({
            'timestamp': timestamp,
            'message': message
        }))
        self.redis_client.ltrim('orchestrator:logs', 0, 999)  # Keep last 1000 logs
    
    def get_agent_containers(self) -> List[docker.models.containers.Container]:
        """Get all agent containers"""
        try:
            containers = self.docker_client.containers.list(
                filters={'name': 'agent-'}
            )
            return containers
        except Exception as e:
            logger.error(f"Failed to get agent containers: {e}")
            return []
    
    def check_agent_health(self, container) -> Dict:
        """Check health of an agent container"""
        try:
            # Get container stats
            stats = container.stats(stream=False)
            
            # Check if container is running
            container.reload()
            is_running = container.status == 'running'
            
            # Get logs (last 10 lines)
            logs = container.logs(tail=10).decode('utf-8')
            
            return {
                'name': container.name,
                'status': container.status,
                'is_running': is_running,
                'cpu_usage': self._calculate_cpu_usage(stats),
                'memory_usage': self._calculate_memory_usage(stats),
                'recent_logs': logs.split('\n')[-5:] if logs else []
            }
        except Exception as e:
            logger.error(f"Failed to check health for {container.name}: {e}")
            return {
                'name': container.name,
                'status': 'error',
                'is_running': False,
                'error': str(e)
            }
    
    def _calculate_cpu_usage(self, stats) -> float:
        """Calculate CPU usage percentage"""
        try:
            cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - \
                       stats['precpu_stats']['cpu_usage']['total_usage']
            system_delta = stats['cpu_stats']['system_cpu_usage'] - \
                          stats['precpu_stats']['system_cpu_usage']
            
            if system_delta > 0:
                return (cpu_delta / system_delta) * 100.0
            return 0.0
        except (KeyError, ZeroDivisionError):
            return 0.0
    
    def _calculate_memory_usage(self, stats) -> Dict:
        """Calculate memory usage"""
        try:
            memory_usage = stats['memory_stats']['usage']
            memory_limit = stats['memory_stats']['limit']
            memory_percent = (memory_usage / memory_limit) * 100
            
            return {
                'used_mb': memory_usage / (1024 * 1024),
                'limit_mb': memory_limit / (1024 * 1024),
                'percent': memory_percent
            }
        except KeyError:
            return {'used_mb': 0, 'limit_mb': 0, 'percent': 0}
    
    def restart_unhealthy_agents(self):
        """Restart agents that are unhealthy"""
        containers = self.get_agent_containers()
        
        for container in containers:
            health = self.check_agent_health(container)
            
            if not health['is_running'] or health['status'] != 'running':
                self.log_activity(f"🔄 Restarting unhealthy agent: {container.name}")
                try:
                    container.restart()
                    self.log_activity(f"✅ Successfully restarted {container.name}")
                except Exception as e:
                    self.log_activity(f"❌ Failed to restart {container.name}: {e}")
    
    def monitor_agent_communication(self):
        """Monitor agent communication patterns"""
        try:
            # Check message queues
            for project in self.projects:
                for agent_type in self.agent_types:
                    channel = f"agent:{agent_type}:{project}"
                    
                    # Check if agent is responsive (simple ping)
                    test_message = json.dumps({
                        'from': 'orchestrator',
                        'type': 'ping',
                        'timestamp': datetime.now().isoformat()
                    })
                    
                    self.redis_client.publish(channel, test_message)
            
            self.log_activity("📡 Communication health check sent to all agents")
            
        except Exception as e:
            self.log_activity(f"❌ Communication monitoring failed: {e}")
    
    def generate_system_report(self) -> Dict:
        """Generate comprehensive system status report"""
        containers = self.get_agent_containers()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_agents': len(containers),
            'healthy_agents': 0,
            'unhealthy_agents': 0,
            'agents': []
        }
        
        for container in containers:
            health = self.check_agent_health(container)
            report['agents'].append(health)
            
            if health['is_running'] and health.get('status') == 'running':
                report['healthy_agents'] += 1
            else:
                report['unhealthy_agents'] += 1
        
        # Store report in Redis
        self.redis_client.setex(
            'orchestrator:system_report', 
            300,  # 5 minutes TTL
            json.dumps(report)
        )
        
        return report
    
    def scale_agents_if_needed(self):
        """Auto-scale agents based on workload (basic implementation)"""
        # This would contain logic to spawn additional agents
        # if workload is high or remove agents if workload is low
        
        containers = self.get_agent_containers()
        expected_agents = len(self.projects) * len(self.agent_types)
        
        if len(containers) < expected_agents:
            self.log_activity(f"⚠️ Agent count below expected: {len(containers)}/{expected_agents}")
        elif len(containers) > expected_agents:
            self.log_activity(f"ℹ️ Agent count above expected: {len(containers)}/{expected_agents}")
        else:
            self.log_activity(f"✅ Agent count optimal: {len(containers)}/{expected_agents}")
    
    async def orchestration_cycle(self):
        """Main orchestration cycle"""
        cycle_count = 0
        
        while True:
            cycle_count += 1
            self.log_activity(f"=== ORCHESTRATION CYCLE #{cycle_count} ===")
            
            try:
                # Monitor agent health
                self.restart_unhealthy_agents()
                
                # Check communication
                self.monitor_agent_communication()
                
                # Generate system report
                report = self.generate_system_report()
                self.log_activity(f"📊 System Report: {report['healthy_agents']}/{report['total_agents']} agents healthy")
                
                # Auto-scaling check
                self.scale_agents_if_needed()
                
                self.log_activity(f"Orchestration cycle #{cycle_count} complete - next in 60 seconds")
                
            except Exception as e:
                self.log_activity(f"💥 Orchestration cycle failed: {e}")
            
            await asyncio.sleep(60)  # Orchestrator cycles every minute

async def main():
    orchestrator = ContainerizedOrchestrator()
    
    try:
        await orchestrator.orchestration_cycle()
    except KeyboardInterrupt:
        orchestrator.log_activity("🛑 Orchestrator stopped by user")
    except Exception as e:
        orchestrator.log_activity(f"💥 Orchestrator crashed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())