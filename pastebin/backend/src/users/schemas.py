from typing import Optional

from pydantic import BaseModel, EmailStr


class UserEdit(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
