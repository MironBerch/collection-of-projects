from uuid import UUID

import orjson
from pydantic import BaseModel


class OrjsonMixin(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class UUIDMixin(BaseModel):
    uuid: UUID
