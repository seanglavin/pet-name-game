import os
from dotenv import load_dotenv

from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME: str = "pet-name-game"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST","localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT",5432) # default postgres port is 5432
    POSTGRES_DB: str = os.getenv("POSTGRES_DB","tdd")
    DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    PETFINDER_API_KEY: str = os.getenv("PETFINDER_API_KEY")
    PETFINDER_API_SECRET: str = os.getenv("PETFINDER_API_SECRET")

settings = Settings()