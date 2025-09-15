from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import json
import os
from datetime import datetime
import uuid

app = FastAPI(title="Tmux Orchestrator API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory storage (replace with PostgreSQL in production)
projects_db = {}
agents_db = {}

class Project(BaseModel):
    name: str
    description: str
    project_type: str
    project_path: str
    cpu_limit: float = 2.0
    memory_limit: str = "4Gi"
    storage_limit: str = "10Gi"
    auto_start: bool = True
    auto_scale: bool = False
    tags: Dict = {}
    metadata: Dict = {}

class ProjectUpdate(BaseModel):
    status: Optional[str] = None
    manager_cycle: Optional[int] = None

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/projects")
async def get_projects():
    return list(projects_db.values())

@app.get("/api/projects/{project_id}")
async def get_project(project_id: str):
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    return projects_db[project_id]

@app.post("/api/projects")
async def create_project(project: Project):
    project_id = str(uuid.uuid4())
    project_data = {
        **project.dict(),
        "id": project_id,
        "project_id": f"{project.name.lower().replace(' ', '-')}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "last_heartbeat": None,
        "config_version": 1,
        "internal_ip": None,
        "api_port": None,
        "tmux_port": None
    }
    projects_db[project_id] = project_data
    return project_data

@app.put("/api/projects/{project_id}")
async def update_project(project_id: str, update: ProjectUpdate):
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")

    project = projects_db[project_id]
    if update.status:
        project["status"] = update.status
    if update.manager_cycle:
        project["manager_cycle"] = update.manager_cycle

    project["updated_at"] = datetime.now().isoformat()
    projects_db[project_id] = project
    return project

@app.delete("/api/projects/{project_id}")
async def delete_project(project_id: str):
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")

    deleted_project = projects_db.pop(project_id)
    return {"message": "Project deleted", "project": deleted_project}

@app.get("/api/agents")
async def get_agents():
    return list(agents_db.values())

@app.post("/api/agents/{agent_id}/heartbeat")
async def agent_heartbeat(agent_id: str):
    if agent_id not in agents_db:
        agents_db[agent_id] = {
            "id": agent_id,
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }

    agents_db[agent_id]["last_heartbeat"] = datetime.now().isoformat()
    agents_db[agent_id]["status"] = "active"
    return {"message": "Heartbeat received"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)