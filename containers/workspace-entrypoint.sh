#!/bin/bash

# Workspace initialization script
# Sets up project-specific environment based on PROJECT_TYPE

set -e

echo "🏗️  Initializing workspace for ${PROJECT_NAME}"
echo "Project Type: ${PROJECT_TYPE}"

cd /workspace

# Initialize git repository if not exists
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository"
    git init
    echo "# ${PROJECT_NAME}" > README.md
    git add README.md
    git commit -m "Initial commit: workspace setup"
fi

# Set up project structure based on type
case "$PROJECT_TYPE" in
    "nodejs")
        echo "📦 Setting up Node.js project structure"
        if [ ! -f "package.json" ]; then
            cat > package.json << EOF
{
  "name": "${PROJECT_NAME}",
  "version": "1.0.0",
  "description": "Autonomous development project",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js",
    "test": "jest"
  },
  "dependencies": {
    "express": "^4.18.2"
  },
  "devDependencies": {
    "nodemon": "^3.0.1",
    "jest": "^29.0.0"
  }
}
EOF
            echo "Created package.json"
        fi
        
        # Create basic project structure
        mkdir -p src public test
        if [ ! -f "src/index.js" ]; then
            cat > src/index.js << EOF
const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => {
    res.json({ message: 'Hello from ${PROJECT_NAME}!' });
});

app.listen(PORT, () => {
    console.log(\`Server running on port \${PORT}\`);
});
EOF
            echo "Created basic Express server"
        fi
        ;;
        
    "python")
        echo "🐍 Setting up Python project structure"
        if [ ! -f "requirements.txt" ]; then
            cat > requirements.txt << EOF
fastapi==0.104.1
uvicorn==0.24.0
requests==2.31.0
pytest==7.4.3
EOF
            echo "Created requirements.txt"
        fi
        
        # Create Python project structure
        mkdir -p src tests
        if [ ! -f "src/main.py" ]; then
            cat > src/main.py << EOF
from fastapi import FastAPI

app = FastAPI(title="${PROJECT_NAME}")

@app.get("/")
def read_root():
    return {"message": "Hello from ${PROJECT_NAME}!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF
            echo "Created basic FastAPI application"
        fi
        
        # Set up virtual environment
        if [ ! -d "venv" ]; then
            python3 -m venv venv
            source venv/bin/activate
            pip install -r requirements.txt
            echo "Created Python virtual environment"
        fi
        ;;
        
    *)
        echo "ℹ️  Generic project setup"
        mkdir -p src docs tests
        ;;
esac

# Create .gitignore
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << EOF
node_modules/
venv/
__pycache__/
.env
*.log
.DS_Store
dist/
build/
coverage/
EOF
    echo "Created .gitignore"
fi

echo "✅ Workspace initialization complete"

# Execute the provided command or keep container running
exec "$@"