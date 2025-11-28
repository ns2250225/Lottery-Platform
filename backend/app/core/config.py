from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "抽奖应用"
    VERSION: str = "1.0.0"
    DATABASE_URL: str = "sqlite:///./raffle.db"
    ALLOWED_HOSTS: List[str] = ["*"]
    
    class Config:
        env_file = ".env"

settings = Settings()