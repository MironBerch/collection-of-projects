from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import AsyncGenerator


DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/postgres"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
