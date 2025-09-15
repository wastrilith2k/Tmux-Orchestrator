from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from datetime import datetime

app = FastAPI(
    title="Tmux Orchestrator Hub API",
    description="Central API for managing distributed tmux orchestrator projects",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Tmux Orchestrator Hub API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@app.get("/api/projects")
async def list_projects():
    # Placeholder - will be replaced with database integration
    return []

@app.get("/api/system/status")
async def get_system_status():
    return {
        "total_projects": 0,
        "active_projects": 0,
        "total_agents": 0,
        "active_agents": 0,
        "total_messages_today": 0,
        "system_cpu_usage": 0.0,
        "system_memory_usage": 0.0,
        "uptime_seconds": 0
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)