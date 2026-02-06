from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Financial Health Assessment Tool"
    PROJECT_VERSION: str = "0.1.0"
    
    # Database
    # Default to a local Postgres connection, or override with env var
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "finance_db"
    
    @property
    def DATABASE_URL(self) -> str:
        # Use SQLite for local development if standard postgres port is not accessible or just as default
        # For this fix, we force SQLite as requested
        return "sqlite:///./sql_app.db"
    
    # Security
    SECRET_KEY: str = "CHANGE_THIS_IN_PRODUCTION_SECRET_KEY_123"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()
