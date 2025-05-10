import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    # API Settings
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    PROJECT_NAME: str = "Anxiety Ally"
    
    # Authentication
    SECRET_KEY: str = os.getenv("SECRET_KEY", "devkey_change_in_production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    
    # Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    
    # AI Service
    HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY", "")
    MODEL_ENDPOINT: str = os.getenv("MODEL_ENDPOINT", "")
    
    # Redis for caching and rate limiting
    REDIS_URL: str = os.getenv("REDIS_URL", "")
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60  # seconds
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",  # Local frontend development
        "https://anxiety-ally.vercel.app",  # Production frontend
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create a global settings object
settings = Settings() 