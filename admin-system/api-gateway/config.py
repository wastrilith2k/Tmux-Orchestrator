from pydantic_settings import BaseSettings
from typing import List, Union
import os

class Settings(BaseSettings):
    # Database configuration
    database_url: str = "postgresql://admin:orchestrator_pass@postgres:5432/orchestrator_hub"

    # Redis configuration
    redis_url: str = "redis://redis:6379"

    # Security settings
    jwt_secret: str = "dev_secret_key_change_in_production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24

    # CORS settings
    cors_origins: Union[List[str], str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://admin-dashboard:3000"
    ]

    # Application settings
    environment: str = "development"
    debug: bool = True
    log_level: str = "INFO"

    # Hub configuration
    hub_max_projects: int = 50
    project_default_cpu_limit: float = 2.0
    project_default_memory_limit: str = "4Gi"
    project_session_timeout_hours: int = 24

    # Monitoring
    metrics_enabled: bool = True
    health_check_interval: int = 30

    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list, handling both string and list formats."""
        if isinstance(self.cors_origins, str):
            return [origin.strip() for origin in self.cors_origins.split(',') if origin.strip()]
        return self.cors_origins

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Global settings instance
settings = Settings()