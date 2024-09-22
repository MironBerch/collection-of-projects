from uuid import UUID

import orjson
from pydantic import BaseModel


class OrjsonMixin(BaseModel):
    class Config:
        json_load = orjson.loads
        json_dump = orjson.dumps


class UUIDMixin(BaseModel):
    uuid: UUID
