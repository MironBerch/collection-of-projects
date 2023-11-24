from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel, EmailStr


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    username: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserEdit(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None


class ForgotPassword(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    password: str


class ChangePassword(BaseModel):
    old_password: str
    new_password: str
