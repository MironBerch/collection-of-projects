class Config():
    """Класс с настройками для датакласса на основе `pydantic`."""

    arbitrary_types_allowed = True


class UpdatesNotFoundError(Exception):
    """Обновлений не обнаружено."""
