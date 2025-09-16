#!/usr/bin/env python3
"""
Health check script for orchestrator container
"""

import redis
import sys
import os

def main():
    try:
        # Check Redis connection
        redis_url = os.getenv('REDIS_URL', 'redis://redis:6379')
        redis_client = redis.from_url(redis_url)
        redis_client.ping()
        
        # Check if orchestrator logs are being updated
        logs = redis_client.lrange('orchestrator:logs', 0, 0)
        if not logs:
            print("No orchestrator logs found")
            sys.exit(1)
        
        print("Orchestrator healthy")
        sys.exit(0)
        
    except Exception as e:
        print(f"Health check failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()