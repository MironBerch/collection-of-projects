from os import environ

from pydantic import Field
from pydantic_settings import BaseSettings


class TelegramConfig(BaseSettings):
    api_token: str = environ.get('TELEGRAM_API_TOKEN')


class Settings(BaseSettings):
    telegram: TelegramConfig = Field(default_factory=TelegramConfig)


settings = Settings()
