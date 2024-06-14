from pydantic import BaseModel


class CreatePost(BaseModel):
    text: int

    class Config:
        orm_mode = True


class Post(BaseModel):
    id: int
    text: int

    class Config:
        orm_mode = True
