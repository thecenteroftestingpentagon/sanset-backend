from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "Sanset FastAPI Backend"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = "your-secret-key-change-in-production-min-32-chars-long"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 43200
    
    DATABASE_URL: str = "sqlite:///./sanset.db"
    
    PORT: int = 5000
    HOST: str = "0.0.0.0"
    
    SENTRY_DSN: Optional[str] = None
    
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
