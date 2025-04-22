from pydantic import BaseModel


class TaskCreate(BaseModel):
    text: str


class Task(BaseModel):
    id: int
    text: str

    class Config:
        orm_mode = True
