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

Settings.DATABASE_URL="postgresql://neondb_owner:WjPvXaecO0k3@ep-shy-sun-a6njkfhz.us-west-2.aws.neon.tech/neondb?sslmode=require"
