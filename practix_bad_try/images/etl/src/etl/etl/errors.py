class ExtractError(Exception):
    """Ошибка при извлечении данных."""


class ExtractConnectionError(ExtractError):
    """Ошибка подключения с источником данных."""

    def __init__(self, detail: str):
        self.message = f'Нет подключения к отправителю данных!\nПричина: {detail}'
        super().__init__(self.message)


class ExtractTableError(ExtractError):
    """Ошибка таблицы источника данных."""

    def __init__(self, detail: str):
        self.message = f'Данные не были извлечены!\nПричина: {detail}'
        super().__init__(self.message)


class TransformError(Exception):
    """Ошибка при преобразовании данных."""

    def __init__(self, errors: list, index: str):
        """
        При инициализации исключения ожидает данные об ошибке и номер строки, где была ошибка.
        """
        column = errors[0]['loc'][0]
        message = errors[0]['msg']
        self.message = \
            f'Ошибка валидации:\n- колонка: {column}\n- сообщение: {message}\n- строка: {index}\n'
        super().__init__(self.message)


class LoadError(Exception):
    """Ошибка при загрузке данных."""


class LoadConnectionError(LoadError):
    """Ошибка подключения с получателем данных."""

    def __init__(self, detail: str):
        self.message = f'Нет подключения к получателю данных!\nПричина: {detail}'
        super().__init__(self.message)


class LoadTableError(LoadError):
    """Ошибка таблицы получателя данных."""

    def __init__(self, detail: str):
        self.message = f'Данные не были загружены!\nПричина: {detail}'
        super().__init__(self.message)
