from telegram.ext import Application, CommandHandler

HANDLERS = {}


def initialize_handlers(application: Application) -> None:
    """
    Initialize telegram handlers.

    Args:
        application (telegram.ext.Application): telegram application object.

    Returns:
        None:
    """
    for command, callback in HANDLERS.items():
        application.add_handler(CommandHandler(command, callback))
