from functools import wraps
from time import sleep
from typing import Any, Callable

from core.logger import logger


def backoff(exceptions: tuple[Exception], sleep_time: float = 1.0) -> Callable:
    """Функция для повторного выполнения функции через некоторое время, если возникла ошибка."""
    def decorator(func) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            while True:
                try:
                    connection = func(*args, **kwargs)
                except exceptions as message:
                    logger.error(f'Нет соединения: {message}')
                    logger.error(f'Повторное подключение через {sleep_time}с')
                    sleep(sleep_time)
                else:
                    return connection
        return wrapper
    return decorator
