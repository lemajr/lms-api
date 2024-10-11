import os
from pydantic_settings import BaseSettings


# Load environment variables from .env file
class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    DATABASE_URL: str

    class Config:
        env_file = '.env.local'

settings = Settings()  

settings.DATABASE_URL="postgresql://lemajr:lemajr@localhost:5432/lms_db"
