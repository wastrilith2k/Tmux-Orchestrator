#!/usr/bin/env python3

"""
Real-time Claude Agent Approval Monitor
Continuously watches for approval dialogs and automatically learns from them
"""

import time
import signal
import sys
from pathlib import Path
from claude_agent_manager import ClaudeAgentManager
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/approval_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('ApprovalMonitor')

class ApprovalMonitor:
    def __init__(self, check_interval: int = 5):
        self.agent_manager = ClaudeAgentManager()
        self.check_interval = check_interval
        self.running = True
        self.stats = {
            'total_approvals': 0,
            'commands_learned': 0,
            'sessions_monitored': set()
        }
        
    def signal_handler(self, signum, frame):
        """Handle shutdown gracefully"""
        logger.info("Received shutdown signal, stopping monitor...")
        self.running = False
        
    def monitor_loop(self):
        """Main monitoring loop"""
        logger.info(f"🔍 Starting approval monitor (checking every {self.check_interval}s)")
        logger.info("Press Ctrl+C to stop monitoring")
        
        while self.running:
            try:
                # Get all current sessions
                sessions = self.agent_manager.get_tmux_sessions()
                current_sessions = {session.name for session in sessions}
                
                # Track new sessions
                new_sessions = current_sessions - self.stats['sessions_monitored']
                if new_sessions:
                    logger.info(f"📊 Monitoring new sessions: {', '.join(new_sessions)}")
                    self.stats['sessions_monitored'].update(new_sessions)
                
                # Monitor all Claude agents
                approvals_this_cycle = self.agent_manager.auto_approve_all_agents()
                if approvals_this_cycle > 0:
                    self.stats['total_approvals'] += approvals_this_cycle
                    self.stats['commands_learned'] += approvals_this_cycle
                    
                    logger.info(f"📈 Total approvals: {self.stats['total_approvals']}, Commands learned: {self.stats['commands_learned']}")
                
                # Show status every 10 cycles
                if self.stats['total_approvals'] > 0 and self.stats['total_approvals'] % 10 == 0:
                    self.show_status()
                    
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                logger.info("Monitor stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(self.check_interval)
        
        self.show_final_stats()
    
    def show_status(self):
        """Show current monitoring status"""
        logger.info("=" * 50)
        logger.info(f"📊 Approval Monitor Status")
        logger.info(f"   Total approvals processed: {self.stats['total_approvals']}")
        logger.info(f"   Commands learned: {self.stats['commands_learned']}")
        logger.info(f"   Sessions monitored: {len(self.stats['sessions_monitored'])}")
        logger.info(f"   Active sessions: {', '.join(self.stats['sessions_monitored'])}")
        logger.info("=" * 50)
    
    def show_final_stats(self):
        """Show final statistics"""
        logger.info("🏁 Approval Monitor Final Statistics:")
        logger.info(f"   Total approvals processed: {self.stats['total_approvals']}")
        logger.info(f"   Commands learned and added to configs: {self.stats['commands_learned']}")
        logger.info(f"   Sessions monitored: {len(self.stats['sessions_monitored'])}")
        
        if self.stats['total_approvals'] > 0:
            logger.info("✅ Agent configurations have been enhanced with learned approvals")
        else:
            logger.info("ℹ️  No approval dialogs were detected during monitoring")
    
    def list_learned_commands(self, session_name: str):
        """Show all commands learned for a specific session"""
        try:
            config_file = Path.home() / f".claude-agent-{session_name}.json"
            if not config_file.exists():
                logger.warning(f"No config file found for session: {session_name}")
                return
                
            import json
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            # Find project configurations
            for project_path, project_config in config.get('projects', {}).items():
                if 'autoApproveCommands' in project_config:
                    logger.info(f"📝 Learned commands for {project_path}:")
                    for command, approved in project_config['autoApproveCommands'].items():
                        if approved:
                            logger.info(f"   ✅ {command}")
                            
        except Exception as e:
            logger.error(f"Error reading learned commands: {e}")

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Monitor Claude agents for approval dialogs')
    parser.add_argument('--interval', '-i', type=int, default=5, 
                       help='Check interval in seconds (default: 5)')
    parser.add_argument('--list-commands', '-l', type=str, 
                       help='List learned commands for a specific session')
    parser.add_argument('--daemon', '-d', action='store_true',
                       help='Run as background daemon')
    
    args = parser.parse_args()
    
    monitor = ApprovalMonitor(check_interval=args.interval)
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, monitor.signal_handler)
    signal.signal(signal.SIGTERM, monitor.signal_handler)
    
    if args.list_commands:
        monitor.list_learned_commands(args.list_commands)
        return
    
    if args.daemon:
        logger.info("Running in daemon mode...")
        # In a real implementation, you'd fork here
        
    try:
        monitor.monitor_loop()
    except KeyboardInterrupt:
        logger.info("Monitor stopped")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()