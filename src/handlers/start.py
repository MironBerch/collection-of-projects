from telegram import Update
from telegram.ext import ContextTypes

from utils.response import send_response
from utils.templates import render_template


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await send_response(
        update,
        context,
        response=render_template(
            template_name='start.j2',
            data={},
        ),
    )
