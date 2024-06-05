from pydantic import BaseModel


class CreatePost(BaseModel):
    text: int

    class Config:
        from_attributes = True


class Post(BaseModel):
    id: int
    text: int

    class Config:
        from_attributes = True
