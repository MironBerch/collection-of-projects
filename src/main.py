import logging
from typing import Any

from telegram.ext import Application, ApplicationBuilder, CommandHandler

from commands import COMMAND_HANDLERS
from config import TELEGRAM_API_TOKEN


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


if not TELEGRAM_API_TOKEN:
    raise ValueError(
        'TELEGRAM_API_TOKEN env variables was not implemented in .env.',
    )


def main() -> None:
    application: Application[Any, Any, Any, Any, Any, Any] = (
        ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()
    )

    for command_name, command_handler in COMMAND_HANDLERS.items():
        application.add_handler(CommandHandler(command_name, command_handler))

    application.run_polling()


if __name__ == '__main__':
    try:
        main()
    except Exception:
        import traceback

        logger.warning(traceback.format_exc())
