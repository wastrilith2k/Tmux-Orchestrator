#!/bin/bash

# Deploy Fully Containerized Tmux Orchestrator
# This script builds and deploys the complete containerized autonomous agent system

set -e

echo "🐳 DEPLOYING FULLY CONTAINERIZED TMUX ORCHESTRATOR"
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose > /dev/null 2>&1; then
    echo "❌ docker-compose is not installed. Please install docker-compose first."
    exit 1
fi

echo "✅ Docker environment verified"

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose -f docker-compose.containerized.yml down || true

# Remove existing images to force rebuild
echo "🧹 Cleaning up existing images..."
docker images | grep tmux-orchestrator | awk '{print $3}' | xargs -r docker rmi -f || true

# Build all container images
echo "🔨 Building container images..."
docker-compose -f docker-compose.containerized.yml build --no-cache

echo "🚀 Starting containerized autonomous agent system..."

# Start infrastructure first
echo "📡 Starting infrastructure services..."
docker-compose -f docker-compose.containerized.yml up -d postgres redis api-gateway

# Wait for infrastructure to be healthy
echo "⏳ Waiting for infrastructure to be ready..."
sleep 10

# Check infrastructure health
echo "🏥 Checking infrastructure health..."
for service in postgres redis; do
    echo "Checking $service..."
    timeout 30 bash -c "until docker-compose -f docker-compose.containerized.yml exec $service echo 'ready'; do sleep 1; done" || {
        echo "❌ $service failed to start properly"
        exit 1
    }
done

# Start workspace containers
echo "🏗️  Starting workspace containers..."
docker-compose -f docker-compose.containerized.yml up -d \
    workspace-test-todo \
    workspace-ml-pipeline \
    workspace-ecommerce

sleep 5

# Start agent containers
echo "🤖 Starting autonomous agent containers..."
docker-compose -f docker-compose.containerized.yml up -d \
    engineer-test-todo pm-test-todo qa-test-todo devops-test-todo \
    engineer-ml pm-ml \
    engineer-ecommerce pm-ecommerce

# Start orchestrator
echo "🎯 Starting agent orchestrator..."
docker-compose -f docker-compose.containerized.yml up -d orchestrator

# Show status
sleep 10
echo ""
echo "📊 CONTAINERIZED SYSTEM STATUS"
echo "=============================="

echo ""
echo "🐳 Container Status:"
docker-compose -f docker-compose.containerized.yml ps

echo ""
echo "📡 Infrastructure Services:"
echo "  - PostgreSQL: http://localhost:5432"
echo "  - Redis: http://localhost:6379" 
echo "  - API Gateway: http://localhost:8080"

echo ""
echo "🤖 Autonomous Agents:"
docker ps --filter "name=agent-" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "🏗️  Project Workspaces:"
docker ps --filter "name=workspace-" --format "table {{.Names}}\t{{.Status}}"

echo ""
echo "📈 System Monitoring:"
echo "  - Orchestrator logs: docker logs agent-orchestrator"
echo "  - Agent logs: docker logs <agent-name>"
echo "  - System stats: docker stats"

echo ""
echo "🎉 CONTAINERIZED DEPLOYMENT COMPLETE!"
echo "======================================"
echo ""
echo "All agents are now running in isolated Docker containers with:"
echo "✅ Redis pub/sub communication (no direct tmux dependency)"
echo "✅ Isolated project workspaces with persistent volumes"
echo "✅ Automated agent health monitoring and restart"
echo "✅ Container orchestration and scaling capabilities"
echo "✅ Complete separation from host system"
echo ""
echo "To monitor the system:"
echo "  docker-compose -f docker-compose.containerized.yml logs -f"
echo ""
echo "To stop the system:"
echo "  docker-compose -f docker-compose.containerized.yml down"