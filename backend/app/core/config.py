from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Astra AI"
    API_V1_STR: str = "/api"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./compliance_copilot.db")
    CORS_ORIGINS: List[str] = ["*"]
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "auto")

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
