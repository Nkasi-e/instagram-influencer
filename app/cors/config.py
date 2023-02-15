from pydantic import BaseSettings
from pathlib import Path


PARENT_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    JWT_SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRATION: str

    class Config:
        env_file = f'{PARENT_DIR}/.env'


settings = Settings()
