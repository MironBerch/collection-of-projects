from telegram.ext import ApplicationBuilder

from core.logger import logger
from core.config import settings


def main():
    application = ApplicationBuilder().token(settings.telegram.api_token).build()
    application.run_polling()


if __name__ == '__main__':
    try:
        main()
    except Exception:
        import traceback
        logger.warning(traceback.format_exc())
