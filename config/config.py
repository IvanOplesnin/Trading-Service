from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):
    db_url: str
    jwt_secret: str
    jwt_expire_minutes: int = 60
    environment: str = "dev"

    class Config:
        env_file = ENV_PATH


settings = Settings()  # type: ignore
