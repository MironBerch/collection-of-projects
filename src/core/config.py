from os import environ
from pathlib import Path, PosixPath

from pydantic import Field
from pydantic_settings import BaseSettings


class TelegramConfig(BaseSettings):
    api_token: str = environ.get('TELEGRAM_API_TOKEN')


class Settings(BaseSettings):
    telegram: TelegramConfig = Field(default_factory=TelegramConfig)
    templates_dir: PosixPath = Path(__file__).resolve().parent.parent / 'templates'


settings = Settings()
