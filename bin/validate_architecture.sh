#!/bin/bash

# Tmux Orchestrator - Architecture Validation & Setup Script
# Ensures components are properly distributed between host and containers

echo "🏗️ TMUX ORCHESTRATOR - ARCHITECTURE VALIDATION"
echo "================================================"

# 1. VALIDATE HOST COMPONENTS (Should NOT be in containers)
echo "📍 1. VALIDATING HOST COMPONENTS..."

# Check agents (should be in tmux on host)
echo "   🤖 Agent Sessions:"
if tmux list-sessions 2>/dev/null | grep -E "(proj-|pm-|qa-|devops-)" | wc -l | grep -q "[1-9]"; then
    echo "   ✅ Agents running on host in tmux (CORRECT)"
    tmux list-sessions | grep -E "(proj-|pm-|qa-|devops-)" | sed 's/^/      /'
else
    echo "   ⚠️ No agents running in tmux"
fi

# Check orchestrator (should be on host for tmux control)
echo "   🎯 Orchestrator:"
if pgrep -f "hub_orchestrator.py" >/dev/null; then
    echo "   ✅ Orchestrator running on host (CORRECT)"
else
    echo "   ⚠️ Orchestrator not running"
fi

# Check project files (should be on host filesystem)
echo "   📁 Project Files:"
if [ -d "/home/james/test-projects" ] && [ "$(ls -A /home/james/test-projects/)" ]; then
    echo "   ✅ Projects on host filesystem (CORRECT)"
    ls /home/james/test-projects/ | sed 's/^/      /'
else
    echo "   ⚠️ No projects found on host"
fi

echo

# 2. VALIDATE CONTAINERIZED COMPONENTS (Should be in Docker)
echo "📦 2. VALIDATING CONTAINERIZED INFRASTRUCTURE..."

# Check for Docker
if command -v docker >/dev/null 2>&1; then
    echo "   🐳 Docker: Available"

    # Check hub infrastructure containers
    echo "   🏭 Hub Infrastructure:"
    if docker ps --format "table {{.Names}}\t{{.Status}}" 2>/dev/null | grep -E "(postgres|redis|gateway|dashboard)" | wc -l | grep -q "[1-9]"; then
        echo "   ✅ Infrastructure containers running (CORRECT)"
        docker ps --format "   {{.Names}}: {{.Status}}" | grep -E "(postgres|redis|gateway|dashboard)"
    else
        echo "   ⚠️ Infrastructure containers not running"
        echo "   📝 SHOULD BE CONTAINERIZED:"
        echo "      - PostgreSQL (database)"
        echo "      - Redis (caching/queues)"
        echo "      - API Gateway (hub coordination)"
        echo "      - Dashboard (monitoring UI)"
    fi
else
    echo "   ❌ Docker not available"
    echo "   📝 INFRASTRUCTURE SHOULD RUN IN DOCKER:"
    echo "      - PostgreSQL (database)"
    echo "      - Redis (caching/queues)"
    echo "      - API Gateway (hub coordination)"
    echo "      - Dashboard (monitoring UI)"
fi

echo

# 3. ARCHITECTURE RECOMMENDATIONS
echo "📋 3. ARCHITECTURE RECOMMENDATIONS"
echo "=================================="

echo "✅ CORRECT: Keep on Host"
echo "   • Agent processes (tmux sessions)"
echo "   • Orchestrator (tmux control needed)"
echo "   • Project files (direct git access)"
echo "   • Communication scripts"
echo ""

echo "🐳 SHOULD BE CONTAINERIZED:"
echo "   • PostgreSQL database"
echo "   • Redis cache/message queue"
echo "   • API Gateway (FastAPI/Node.js)"
echo "   • Dashboard UI (React/Next.js)"
echo "   • Log aggregation (optional)"
echo ""

echo "🔄 HYBRID COMMUNICATION:"
echo "   • Agents ↔ Hub: HTTP API calls"
echo "   • Agent ↔ Agent: tmux send-keys"
echo "   • Hub ↔ Containers: Docker networking"
echo ""

# 4. CURRENT STATUS SUMMARY
echo "📊 4. CURRENT STATUS SUMMARY"
echo "============================="

agent_count=$(tmux list-sessions 2>/dev/null | grep -E "(proj-|pm-|qa-|devops-)" | wc -l)
orchestrator_running=$(pgrep -f "hub_orchestrator.py" >/dev/null && echo "YES" || echo "NO")
projects_exist=$([ -d "/home/james/test-projects" ] && [ "$(ls -A /home/james/test-projects/)" ] && echo "YES" || echo "NO")
docker_available=$(command -v docker >/dev/null 2>&1 && echo "YES" || echo "NO")
containers_running=$(docker ps 2>/dev/null | grep -E "(postgres|redis|gateway|dashboard)" | wc -l)

echo "Host Components:"
echo "   • Agents: $agent_count sessions"
echo "   • Orchestrator: $orchestrator_running"
echo "   • Projects: $projects_exist"
echo ""
echo "Container Infrastructure:"
echo "   • Docker: $docker_available"
echo "   • Containers: $containers_running running"
echo ""

if [ $agent_count -gt 0 ] && [ "$orchestrator_running" = "YES" ] && [ "$projects_exist" = "YES" ]; then
    echo "🎉 CONCLUSION: Host components correctly deployed!"
    echo "   Next: Set up containerized hub infrastructure"
else
    echo "⚠️ CONCLUSION: Host components need attention"
fi