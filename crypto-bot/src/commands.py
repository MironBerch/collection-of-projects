from typing import Any

from handlers import start


COMMAND_HANDLERS: dict[str, Any] = {
    'start': start.start,
}
