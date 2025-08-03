from os import environ
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class TelegramConfig(BaseSettings):
    api_token: str | None = environ.get('TELEGRAM_API_TOKEN')


class Settings(BaseSettings):
    telegram: TelegramConfig = Field(default_factory=TelegramConfig)
    templates_dir: Path = Path(__file__).resolve().parent.parent / 'templates'


settings = Settings()
