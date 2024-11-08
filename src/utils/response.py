from typing import cast

import telegram
from telegram import Chat, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


def _get_chat_id(update: Update) -> int:
    """
    Get chat id.

    Args:
        update (telegram.Update): incoming update.

    Returns:
        int: chat id.
    """
    return cast(Chat, update.effective_chat).id


async def send_response(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    response: str,
    keyboard: InlineKeyboardMarkup | None = None,
) -> None:
    """
    Send telegram response use html render.

    Args:
        update (telegram.Update): incoming update.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): context for the default settings.

    Returns:
        None:
    """
    args = {
        'chat_id': _get_chat_id(update),
        'disable_web_page_preview': True,
        'text': response,
        'parse_mode': telegram.constants.ParseMode.HTML,
    }

    if keyboard:
        args['reply_markup'] = keyboard

    await context.bot.send_message(**args)
