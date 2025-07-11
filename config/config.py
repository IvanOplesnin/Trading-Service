from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):
    db_url: str = "postgresql+asyncpg://fake:fake@localhost:5432/trading_db"
    jwt_secret: str = "fake-secret"
    jwt_expire_minutes: int = 300
    jwt_algorithm: str = "HS256"
    environment: str = "dev"

    model_config = SettingsConfigDict(env_file=ENV_PATH, env_file_encoding="utf-8")


settings = Settings()
