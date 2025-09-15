#!/bin/bash
# Tmux Orchestrator Hub Management Script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HUB_DIR="$SCRIPT_DIR/../admin-system"
ENV_FILE="$HUB_DIR/.env"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_dependencies() {
    log_info "Checking dependencies..."

    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi

    log_success "All dependencies are installed"
}

setup_environment() {
    log_info "Setting up environment..."

    if [ ! -f "$ENV_FILE" ]; then
        log_info "Creating environment file..."
        cp "$HUB_DIR/.env.example" "$ENV_FILE"

        # Generate secure random passwords
        DB_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)
        JWT_SECRET=$(openssl rand -base64 64 | tr -d "=+/" | cut -c1-50)
        GRAFANA_PASSWORD=$(openssl rand -base64 16 | tr -d "=+/" | cut -c1-12)

        # Update the .env file with secure passwords
        sed -i "s/orchestrator_secure_password_change_me/$DB_PASSWORD/g" "$ENV_FILE"
        sed -i "s/your_jwt_secret_key_change_this_in_production_at_least_32_chars/$JWT_SECRET/g" "$ENV_FILE"
        sed -i "s/admin_change_me/$GRAFANA_PASSWORD/g" "$ENV_FILE"

        log_success "Environment file created with secure passwords"
        log_info "Database password: $DB_PASSWORD"
        log_info "Grafana password: $GRAFANA_PASSWORD"
        log_warning "Please save these passwords securely!"
    else
        log_info "Environment file already exists"
    fi
}

create_bridge_network() {
    log_info "Creating project bridge network..."

    if ! docker network ls | grep -q "tmux-orchestrator-bridge"; then
        docker network create tmux-orchestrator-bridge
        log_success "Bridge network created"
    else
        log_info "Bridge network already exists"
    fi
}

start_hub() {
    log_info "Starting Tmux Orchestrator Hub System..."

    check_dependencies
    setup_environment
    create_bridge_network

    cd "$HUB_DIR"

    # Pull latest images
    log_info "Pulling Docker images..."
    docker-compose -f docker-compose.admin.yml pull

    # Start services
    log_info "Starting services..."
    docker-compose -f docker-compose.admin.yml up -d

    # Wait for services to be ready
    log_info "Waiting for services to start..."
    sleep 15

    # Check health
    check_health
}

stop_hub() {
    log_info "Stopping Hub System..."
    cd "$HUB_DIR"
    docker-compose -f docker-compose.admin.yml down
    log_success "Hub system stopped"
}

restart_hub() {
    log_info "Restarting Hub System..."
    stop_hub
    sleep 5
    start_hub
}

check_health() {
    log_info "Checking system health..."

    # Check if API is responding
    if curl -f -s http://localhost:8080/health > /dev/null; then
        log_success "API Gateway is healthy"
    else
        log_error "API Gateway is not responding"
        return 1
    fi

    # Check if dashboard is accessible
    if curl -f -s http://localhost:3000 > /dev/null; then
        log_success "Dashboard is accessible"
    else
        log_warning "Dashboard may not be ready yet"
    fi

    log_success "Hub system is running!"
    echo ""
    echo "Access points:"
    echo "  Dashboard: http://localhost:3000"
    echo "  API: http://localhost:8080"
    echo "  API Docs: http://localhost:8080/docs"
    echo "  Grafana: http://localhost:3001 (admin/admin)"
    echo "  Prometheus: http://localhost:9090"
    echo ""
}

show_status() {
    log_info "Hub System Status:"
    cd "$HUB_DIR"
    docker-compose -f docker-compose.admin.yml ps
}

show_logs() {
    cd "$HUB_DIR"
    if [ -n "$2" ]; then
        log_info "Showing logs for service: $2"
        docker-compose -f docker-compose.admin.yml logs -f "$2"
    else
        log_info "Showing all service logs:"
        docker-compose -f docker-compose.admin.yml logs -f
    fi
}

cleanup() {
    log_warning "This will remove all containers, volumes, and data. Are you sure? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        log_info "Cleaning up..."
        cd "$HUB_DIR"
        docker-compose -f docker-compose.admin.yml down -v
        docker network rm tmux-orchestrator-bridge 2>/dev/null || true
        log_success "Cleanup complete"
    else
        log_info "Cleanup cancelled"
    fi
}

show_help() {
    echo "Tmux Orchestrator Hub Management"
    echo ""
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  start        Start the hub system"
    echo "  stop         Stop the hub system"
    echo "  restart      Restart the hub system"
    echo "  status       Show service status"
    echo "  health       Check system health"
    echo "  logs [svc]   Show logs (optionally for specific service)"
    echo "  cleanup      Remove all containers and data"
    echo "  help         Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start                    # Start the hub system"
    echo "  $0 logs api-gateway         # Show API gateway logs"
    echo "  $0 health                   # Check if system is healthy"
    echo ""
}

# Main command handling
case "$1" in
    "start")
        start_hub
        ;;
    "stop")
        stop_hub
        ;;
    "restart")
        restart_hub
        ;;
    "status")
        show_status
        ;;
    "health")
        check_health
        ;;
    "logs")
        show_logs "$@"
        ;;
    "cleanup")
        cleanup
        ;;
    "help"|"--help"|"-h")
        show_help
        ;;
    *)
        log_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac