from uuid import UUID

from pydantic import BaseModel


class UUIDMixin(BaseModel):
    """Mixin для моделей с `uuid` первичным ключом."""

    id: UUID
