from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings."""
    # Application Info
    APP_NAME: str = "Product Analyzer API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Analyze product comments: rating, summary, fake-comment detection, and keyword extraction."
    
    # API Settings
    API_PREFIX: str = "/api"
    CORS_ORIGINS: list[str] = ["*"]
    
    # LLM Settings
    GOOGLE_API_KEY: str
    LLM_PROVIDER: str = "gemini"
    LLM_MODEL_NAME: str = "gemini-2.0-flash-lite"
    LLM_TEMPERATURE: float = 0.0
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings() 