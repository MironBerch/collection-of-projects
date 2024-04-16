from os import environ
from pathlib import Path


TELEGRAM_API_TOKEN: str | None = environ.get('TELEGRAM_API_TOKEN')

BASE_DIR = Path(__file__).resolve().parent

TEMPLATES_DIR = BASE_DIR / 'templates'

IO_NET_API_KEY: str | None = environ.get('IO_NET_API_KEY')
