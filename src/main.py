import logging

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from handlers import start, voice
from core.config import settings

COMMAND_HANDLERS = {'start': start.start}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO,
)
logger = logging.getLogger(__name__)


if not settings.telegram.api_token:
    raise ValueError(
        'TELEGRAM_API_TOKEN env variables was not implemented in .env.',
    )


def main():
    application = ApplicationBuilder().token(settings.telegram.api_token).build()

    for command_name, command_handler in COMMAND_HANDLERS.items():
        application.add_handler(CommandHandler(command_name, command_handler))
    
    application.add_handler(MessageHandler(filters.VOICE, voice.handle_voice))

    application.run_polling()


if __name__ == '__main__':
    try:
        main()
    except Exception:
        import traceback

        logger.warning(traceback.format_exc())
