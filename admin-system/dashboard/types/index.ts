export interface Project {
  id: string
  project_id: string
  name: string
  description?: string
  project_type: string
  project_path: string
  status: 'pending' | 'starting' | 'running' | 'stopping' | 'stopped' | 'error'
  created_at: string
  updated_at: string
  last_heartbeat?: string
  cpu_limit: number
  memory_limit: string
  storage_limit: string
  auto_start: boolean
  auto_scale: boolean
  config_version: number
  internal_ip?: string
  api_port?: number
  tmux_port?: number
  tags: Record<string, any>
  metadata: Record<string, any>
}

export interface Agent {
  id: string
  project_id: string
  agent_type: string
  agent_role: string
  agent_name: string
  status: 'inactive' | 'starting' | 'active' | 'busy' | 'error' | 'stopping'
  tmux_session?: string
  tmux_window?: string
  tasks_completed: number
  tasks_failed: number
  average_response_time: number
  last_activity?: string
  cpu_usage_percent: number
  memory_usage_mb: number
  created_at: string
  updated_at: string
}

export interface Message {
  id: string
  message_id: string
  sender_type: string
  sender_id?: string
  recipient_type: string
  recipient_id?: string
  project_id: string
  message_type: 'command' | 'status_request' | 'status_response' | 'error_report' | 'progress_update' | 'heartbeat' | 'shutdown'
  content: string
  metadata: Record<string, any>
  priority: number
  requires_response: boolean
  response_timeout?: number
  status: string
  delivered_at?: string
  expires_at?: string
  created_at: string
}

export interface SystemMetrics {
  total_projects: number
  active_projects: number
  total_agents: number
  active_agents: number
  total_messages_today: number
  system_cpu_usage: number
  system_memory_usage: number
  uptime_seconds: number
}

export interface HealthCheck {
  status: string
  timestamp: string
  database: boolean
  redis: boolean
  version: string
}

export interface ProjectCreateData {
  name: string
  description?: string
  project_type: string
  project_path: string
  cpu_limit?: number
  memory_limit?: string
  storage_limit?: string
  auto_start?: boolean
  auto_scale?: boolean
  tags?: Record<string, any>
  metadata?: Record<string, any>
}