from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from database import get_async_session

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
