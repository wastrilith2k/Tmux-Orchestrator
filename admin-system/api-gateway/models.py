from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ProjectStatus(str, Enum):
    PENDING = "pending"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"

class AgentStatus(str, Enum):
    INACTIVE = "inactive"
    STARTING = "starting"
    ACTIVE = "active"
    BUSY = "busy"
    ERROR = "error"
    STOPPING = "stopping"

class MessageType(str, Enum):
    COMMAND = "command"
    STATUS_REQUEST = "status_request"
    STATUS_RESPONSE = "status_response"
    ERROR_REPORT = "error_report"
    PROGRESS_UPDATE = "progress_update"
    HEARTBEAT = "heartbeat"
    SHUTDOWN = "shutdown"

class Priority(int, Enum):
    HIGH = 1
    NORMAL = 5
    LOW = 10

# Base project models
class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    project_type: str = Field(..., min_length=1, max_length=50)
    project_path: str = Field(..., min_length=1)
    cpu_limit: float = Field(default=2.0, ge=0.1, le=32.0)
    memory_limit: str = Field(default="4Gi")
    storage_limit: str = Field(default="10Gi")
    auto_start: bool = True
    auto_scale: bool = False
    tags: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    project_path: Optional[str] = Field(None, min_length=1)
    status: Optional[ProjectStatus] = None
    cpu_limit: Optional[float] = Field(None, ge=0.1, le=32.0)
    memory_limit: Optional[str] = None
    storage_limit: Optional[str] = None
    auto_start: Optional[bool] = None
    auto_scale: Optional[bool] = None
    tags: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

class Project(ProjectBase):
    id: str
    project_id: str
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime
    last_heartbeat: Optional[datetime] = None
    config_version: int = 1
    internal_ip: Optional[str] = None
    api_port: Optional[int] = None
    tmux_port: Optional[int] = None

    class Config:
        from_attributes = True

# Agent models
class AgentBase(BaseModel):
    agent_type: str = Field(..., min_length=1, max_length=100)
    agent_role: str = Field(..., min_length=1, max_length=100)
    agent_name: str = Field(..., min_length=1, max_length=255)
    tmux_session: Optional[str] = None
    tmux_window: Optional[str] = None

class AgentCreate(AgentBase):
    project_id: str

class Agent(AgentBase):
    id: str
    project_id: str
    status: AgentStatus
    tasks_completed: int = 0
    tasks_failed: int = 0
    average_response_time: int = 0  # milliseconds
    last_activity: Optional[datetime] = None
    cpu_usage_percent: float = 0.0
    memory_usage_mb: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Message models
class MessageBase(BaseModel):
    content: str = Field(..., min_length=1)
    message_type: MessageType = MessageType.COMMAND
    priority: Priority = Priority.NORMAL
    requires_response: bool = False
    response_timeout: Optional[int] = None  # seconds
    metadata: Dict[str, Any] = Field(default_factory=dict)

class MessageCreate(MessageBase):
    recipient_id: Optional[str] = None  # agent_id or "broadcast"

class Message(MessageBase):
    id: str
    message_id: str
    sender_type: str
    sender_id: Optional[str] = None
    recipient_type: str
    recipient_id: Optional[str] = None
    project_id: str
    status: str = "pending"
    delivered_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

# System models
class HealthCheck(BaseModel):
    status: str
    timestamp: datetime
    database: bool
    redis: bool
    version: str

class SystemMetrics(BaseModel):
    total_projects: int
    active_projects: int
    total_agents: int
    active_agents: int
    total_messages_today: int
    system_cpu_usage: float
    system_memory_usage: float
    uptime_seconds: int

class ResourceAllocation(BaseModel):
    project_id: str
    cpu_cores: float
    memory_gb: float
    storage_gb: float
    network_bandwidth_mbps: int = 100
    cpu_usage_percent: float = 0.0
    memory_usage_gb: float = 0.0
    storage_usage_gb: float = 0.0
    cpu_alert_threshold: float = 80.0
    memory_alert_threshold: float = 85.0
    storage_alert_threshold: float = 90.0
    last_updated: datetime

class Event(BaseModel):
    id: str
    event_type: str
    event_category: str
    project_id: Optional[str] = None
    agent_id: Optional[str] = None
    event_data: Dict[str, Any]
    severity: str = "info"
    user_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True