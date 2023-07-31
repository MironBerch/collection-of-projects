from pydantic import BaseModel


class ProfileCreate(BaseModel):
    text: str
    user_id: int
    pronoun: str
    image: bytes


class ProfileUpdate(BaseModel):
    text: str
    user_id: int
    pronoun: str
    image: bytes
