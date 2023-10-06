from typing import Optional

from pydantic import BaseModel


class PasteUser(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class PasteCreate(BaseModel):
    title: Optional[str]
    content: str
    format: Optional[str]
    expire_date: Optional[str]
    private: Optional[bool] = False


class PasteRead(BaseModel):
    user_id: int
    user: PasteUser
    title: str = None
    content: str
    format: str = None
    expire_date: str = None
    private: bool = False

    class Config:
        from_attributes = True
