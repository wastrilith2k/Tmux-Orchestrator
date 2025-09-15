-- Tmux Orchestrator Hub Database Schema
-- This script initializes the PostgreSQL database for the hub system

\c orchestrator_hub;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Projects table - stores registered project orchestrators
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    project_type VARCHAR(50) NOT NULL,
    project_path TEXT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_heartbeat TIMESTAMP WITH TIME ZONE,

    -- Resource allocation
    cpu_limit DECIMAL(4,2) DEFAULT 2.0,
    memory_limit VARCHAR(10) DEFAULT '4Gi',
    storage_limit VARCHAR(10) DEFAULT '10Gi',

    -- Configuration
    config_version INTEGER DEFAULT 1,
    auto_start BOOLEAN DEFAULT true,
    auto_scale BOOLEAN DEFAULT false,

    -- Network configuration
    internal_ip INET,
    api_port INTEGER,
    tmux_port INTEGER,

    -- Metadata
    tags JSONB DEFAULT '{}',
    metadata JSONB DEFAULT '{}'
);

-- Project configurations table - stores generated configurations
CREATE TABLE project_configurations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    config_type VARCHAR(50) NOT NULL, -- 'docker-compose', 'env', 'project-config'
    config_version INTEGER NOT NULL DEFAULT 1,
    config_data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT true
);

-- Agents table - tracks agent instances across projects
CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    agent_type VARCHAR(100) NOT NULL, -- 'orchestrator', 'developer', 'qa', etc.
    agent_role VARCHAR(100) NOT NULL, -- specialized role from Contains Studio
    agent_name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'inactive',
    tmux_session VARCHAR(255),
    tmux_window VARCHAR(255),

    -- Performance metrics
    tasks_completed INTEGER DEFAULT 0,
    tasks_failed INTEGER DEFAULT 0,
    average_response_time INTEGER DEFAULT 0, -- milliseconds
    last_activity TIMESTAMP WITH TIME ZONE,

    -- Resource usage
    cpu_usage_percent DECIMAL(5,2) DEFAULT 0,
    memory_usage_mb INTEGER DEFAULT 0,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Messages table - stores inter-agent and hub communications
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    message_id VARCHAR(255) UNIQUE NOT NULL,
    sender_type VARCHAR(50) NOT NULL, -- 'hub', 'agent', 'user'
    sender_id UUID, -- references agents.id or null for hub/user
    recipient_type VARCHAR(50) NOT NULL,
    recipient_id UUID, -- references agents.id or project.id
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,

    message_type VARCHAR(50) NOT NULL, -- 'command', 'status_request', 'response', etc.
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',

    priority INTEGER DEFAULT 5, -- 1=high, 5=normal, 10=low
    requires_response BOOLEAN DEFAULT false,
    response_timeout INTEGER, -- seconds

    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'delivered', 'failed', 'expired'
    delivered_at TIMESTAMP WITH TIME ZONE,
    expires_at TIMESTAMP WITH TIME ZONE,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- System metrics table - stores performance and health metrics
CREATE TABLE system_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    metric_type VARCHAR(100) NOT NULL,
    metric_name VARCHAR(255) NOT NULL,
    metric_value DECIMAL(15,6) NOT NULL,
    metric_unit VARCHAR(20),

    -- Associated entity
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,

    tags JSONB DEFAULT '{}',
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Events table - audit log for system events
CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_type VARCHAR(100) NOT NULL,
    event_category VARCHAR(50) NOT NULL, -- 'project', 'agent', 'system', 'security'

    project_id UUID REFERENCES projects(id) ON DELETE SET NULL,
    agent_id UUID REFERENCES agents(id) ON DELETE SET NULL,

    event_data JSONB NOT NULL,
    severity VARCHAR(20) DEFAULT 'info', -- 'debug', 'info', 'warn', 'error', 'critical'

    user_id VARCHAR(255), -- for future user management
    ip_address INET,
    user_agent TEXT,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Resource allocations table - tracks resource usage and limits
CREATE TABLE resource_allocations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,

    -- Allocated resources
    cpu_cores DECIMAL(4,2) NOT NULL,
    memory_gb DECIMAL(6,2) NOT NULL,
    storage_gb DECIMAL(8,2) NOT NULL,
    network_bandwidth_mbps INTEGER DEFAULT 100,

    -- Current usage
    cpu_usage_percent DECIMAL(5,2) DEFAULT 0,
    memory_usage_gb DECIMAL(6,2) DEFAULT 0,
    storage_usage_gb DECIMAL(8,2) DEFAULT 0,

    -- Limits and thresholds
    cpu_alert_threshold DECIMAL(5,2) DEFAULT 80.0,
    memory_alert_threshold DECIMAL(5,2) DEFAULT 85.0,
    storage_alert_threshold DECIMAL(5,2) DEFAULT 90.0,

    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_project_id ON projects(project_id);
CREATE INDEX idx_projects_created_at ON projects(created_at);
CREATE INDEX idx_projects_last_heartbeat ON projects(last_heartbeat);

CREATE INDEX idx_agents_project_id ON agents(project_id);
CREATE INDEX idx_agents_status ON agents(status);
CREATE INDEX idx_agents_type_role ON agents(agent_type, agent_role);
CREATE INDEX idx_agents_last_activity ON agents(last_activity);

CREATE INDEX idx_messages_project_id ON messages(project_id);
CREATE INDEX idx_messages_sender ON messages(sender_type, sender_id);
CREATE INDEX idx_messages_recipient ON messages(recipient_type, recipient_id);
CREATE INDEX idx_messages_status ON messages(status);
CREATE INDEX idx_messages_created_at ON messages(created_at);

CREATE INDEX idx_metrics_project_agent ON system_metrics(project_id, agent_id);
CREATE INDEX idx_metrics_type_name ON system_metrics(metric_type, metric_name);
CREATE INDEX idx_metrics_recorded_at ON system_metrics(recorded_at);

CREATE INDEX idx_events_category_type ON events(event_category, event_type);
CREATE INDEX idx_events_project_id ON events(project_id);
CREATE INDEX idx_events_created_at ON events(created_at);

-- Triggers for updating timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_projects_updated_at
    BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_agents_updated_at
    BEFORE UPDATE ON agents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Views for common queries
CREATE VIEW active_projects AS
SELECT
    p.*,
    COUNT(a.id) as agent_count,
    ra.cpu_usage_percent,
    ra.memory_usage_gb,
    ra.storage_usage_gb
FROM projects p
LEFT JOIN agents a ON p.id = a.project_id AND a.status = 'active'
LEFT JOIN resource_allocations ra ON p.id = ra.project_id
WHERE p.status IN ('running', 'active')
GROUP BY p.id, ra.cpu_usage_percent, ra.memory_usage_gb, ra.storage_usage_gb;

CREATE VIEW project_health_summary AS
SELECT
    p.project_id,
    p.name,
    p.status,
    p.last_heartbeat,
    COUNT(CASE WHEN a.status = 'active' THEN 1 END) as active_agents,
    COUNT(CASE WHEN a.status = 'inactive' THEN 1 END) as inactive_agents,
    COUNT(CASE WHEN a.status = 'error' THEN 1 END) as error_agents,
    AVG(a.average_response_time) as avg_response_time,
    MAX(a.last_activity) as last_agent_activity
FROM projects p
LEFT JOIN agents a ON p.id = a.project_id
GROUP BY p.id, p.project_id, p.name, p.status, p.last_heartbeat;

-- Insert default data
INSERT INTO events (event_type, event_category, event_data, severity)
VALUES ('database_initialized', 'system', '{"version": "1.0", "timestamp": "' || NOW() || '"}', 'info');

-- Grant permissions (adjust as needed for production)
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin;