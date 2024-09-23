import os
from pydantic_settings import BaseSettings

# Load environment variables from .env file
class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    DATABASE_URL: str

    class Config:
        env_file = '.env'

settings = Settings()  
