from pydantic import BaseModel


class CreatePost(BaseModel):
    text: str

    class Config:
        from_attributes = True


class Post(BaseModel):
    id: int
    text: str

    class Config:
        from_attributes = True
