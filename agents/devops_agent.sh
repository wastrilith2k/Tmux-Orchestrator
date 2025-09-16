#!/bin/bash

# DevOps Agent for Tmux Orchestrator
# Focuses on deployment, monitoring, and infrastructure

PROJECT_NAME="$1"
PROJECT_PATH="$2"
PM_SESSION="$3"
CYCLE_COUNT=0

log_activity() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] DEVOPS [$PROJECT_NAME]: $1" | tee -a "${PROJECT_PATH}/devops.log"
}

check_deployment_readiness() {
    cd "$PROJECT_PATH"
    local deployment_score=0

    log_activity "🚀 Checking deployment readiness..."

    # Check for deployment configuration files
    if [ -f "Dockerfile" ]; then
        log_activity "✅ Found Dockerfile"
        deployment_score=$((deployment_score + 1))
    else
        log_activity "📝 Creating basic Dockerfile..."
        create_basic_dockerfile
        deployment_score=$((deployment_score + 1))
    fi

    if [ -f "docker-compose.yml" ] || [ -f "docker-compose.yaml" ]; then
        log_activity "✅ Found docker-compose configuration"
        deployment_score=$((deployment_score + 1))
    fi

    # Check for CI/CD configuration
    if [ -d ".github/workflows" ]; then
        log_activity "✅ Found GitHub Actions workflows"
        deployment_score=$((deployment_score + 1))
    elif [ -f ".gitlab-ci.yml" ]; then
        log_activity "✅ Found GitLab CI configuration"
        deployment_score=$((deployment_score + 1))
    else
        log_activity "📝 No CI/CD configuration found"
    fi

    # Environment configuration
    if [ -f ".env.example" ] || [ -f ".env.template" ]; then
        log_activity "✅ Found environment template"
        deployment_score=$((deployment_score + 1))
    else
        log_activity "📝 Creating .env.example..."
        create_env_template
    fi

    log_activity "🚀 Deployment readiness score: $deployment_score/4"
    return $deployment_score
}

create_basic_dockerfile() {
    if [ -f "package.json" ]; then
        # Node.js Dockerfile
        cat > Dockerfile << 'EOF'
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
EOF
        log_activity "📝 Created Node.js Dockerfile"

    elif [ -f "requirements.txt" ]; then
        # Python Dockerfile
        cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "app.py"]
EOF
        log_activity "📝 Created Python Dockerfile"
    fi
}

create_env_template() {
    if [ -f "package.json" ]; then
        cat > .env.example << 'EOF'
# Node.js Environment Variables
NODE_ENV=production
PORT=3000
DATABASE_URL=postgresql://user:pass@localhost:5432/db
JWT_SECRET=your-secret-key
EOF
    elif [ -f "requirements.txt" ]; then
        cat > .env.example << 'EOF'
# Python Environment Variables
FLASK_ENV=production
DATABASE_URL=postgresql://user:pass@localhost:5432/db
SECRET_KEY=your-secret-key
DEBUG=False
EOF
    fi
    log_activity "📝 Created environment template"
}

monitor_system_health() {
    cd "$PROJECT_PATH"
    log_activity "🔍 Monitoring system health..."

    # Check git repository health
    local git_status=$(git status --porcelain 2>/dev/null | wc -l)
    if [ $git_status -gt 20 ]; then
        log_activity "⚠️ WARNING: Many uncommitted files ($git_status)"
    fi

    # Check for large files that shouldn't be committed
    local large_files=$(find . -type f -size +10M -not -path "./.git/*" 2>/dev/null | wc -l)
    if [ $large_files -gt 0 ]; then
        log_activity "⚠️ WARNING: Found $large_files large files (>10MB)"
    fi

    # Check disk usage in project directory
    local disk_usage=$(du -sh . | cut -f1)
    log_activity "💾 Project disk usage: $disk_usage"

    # Check for security issues
    if [ -f ".env" ]; then
        log_activity "🔒 WARNING: .env file present - ensure it's in .gitignore"
        if ! grep -q ".env" .gitignore 2>/dev/null; then
            echo ".env" >> .gitignore
            log_activity "✅ Added .env to .gitignore"
        fi
    fi
}

setup_monitoring() {
    cd "$PROJECT_PATH"
    log_activity "📊 Setting up monitoring configuration..."

    # Create basic health check endpoint documentation
    if [ ! -f "HEALTH_CHECK.md" ]; then
        cat > HEALTH_CHECK.md << 'EOF'
# Health Check Endpoints

## Application Health
- GET `/health` - Basic application health check
- GET `/health/detailed` - Detailed health information

## Monitoring Metrics
- Application uptime
- Response times
- Error rates
- Resource usage

## Alerts
- High error rate (>5%)
- Response time >2s
- Memory usage >80%
- Disk space <10%
EOF
        log_activity "📝 Created health check documentation"
    fi

    # Create basic monitoring script
    if [ ! -f "monitor.sh" ]; then
        cat > monitor.sh << 'EOF'
#!/bin/bash
# Basic monitoring script

echo "=== System Health Check ==="
echo "Timestamp: $(date)"
echo "Disk Usage: $(df -h . | tail -1 | awk '{print $5}')"
echo "Memory Usage: $(free -h | grep Mem | awk '{print $3"/"$2}')"

if command -v curl &> /dev/null; then
    echo "=== Application Health ==="
    curl -s http://localhost:3000/health || echo "Health endpoint not available"
fi
EOF
        chmod +x monitor.sh
        log_activity "📝 Created basic monitoring script"
    fi
}

backup_and_versioning() {
    cd "$PROJECT_PATH"
    log_activity "💾 Managing backups and versioning..."

    # Ensure proper git configuration
    if [ ! -f ".gitattributes" ]; then
        cat > .gitattributes << 'EOF'
# Auto detect text files and perform LF normalization
* text=auto

# Custom for Visual Studio
*.cs     diff=csharp

# Standard to msysgit
*.doc    diff=astextplain
*.DOC    diff=astextplain
*.docx   diff=astextplain
*.DOCX   diff=astextplain
*.dot    diff=astextplain
*.DOT    diff=astextplain
*.pdf    diff=astextplain
*.PDF    diff=astextplain
*.rtf    diff=astextplain
*.RTF    diff=astextplain
EOF
        log_activity "📝 Created .gitattributes file"
    fi

    # Check for proper branching strategy
    local current_branch=$(git branch --show-current 2>/dev/null)
    if [ "$current_branch" = "main" ] || [ "$current_branch" = "master" ]; then
        log_activity "📋 Working on main branch - consider feature branches for development"
    fi
}

report_devops_status() {
    local deployment_score="$1"
    local health_status="$2"

    # Send DevOps report to Project Manager
    local report="DEVOPS REPORT: Deployment=$deployment_score/4, Health=$health_status, Cycle=$CYCLE_COUNT"

    /home/james/projs/Tmux-Orchestrator/send-claude-message.sh "${PM_SESSION}:0" "$report"
    log_activity "📊 Sent DevOps report to Project Manager"
}

main_devops_cycle() {
    while true; do
        CYCLE_COUNT=$((CYCLE_COUNT + 1))

        log_activity "=== DEVOPS CYCLE #$CYCLE_COUNT ==="

        # Core DevOps responsibilities
        check_deployment_readiness
        local deployment_score=$?

        monitor_system_health

        setup_monitoring

        backup_and_versioning

        # Determine overall health status
        local health_status="GOOD"
        if [ $deployment_score -lt 2 ]; then
            health_status="NEEDS_WORK"
        fi

        log_activity "📊 DevOps Assessment: Deployment=$deployment_score/4, Health=$health_status"

        # Report to Project Manager
        report_devops_status "$deployment_score" "$health_status"

        log_activity "Cycle #$CYCLE_COUNT complete - next in 120 seconds"
        sleep 120  # DevOps runs least frequently
    done
}

# Validate inputs
if [ -z "$PROJECT_NAME" ] || [ -z "$PROJECT_PATH" ] || [ -z "$PM_SESSION" ]; then
    echo "Usage: $0 <project_name> <project_path> <pm_session>"
    exit 1
fi

if [ ! -d "$PROJECT_PATH" ]; then
    echo "Error: Project path $PROJECT_PATH does not exist"
    exit 1
fi

log_activity "DevOps Engineer starting for $PROJECT_NAME at $PROJECT_PATH"
log_activity "Reporting to PM session: $PM_SESSION"

# Start DevOps cycle
main_devops_cycle