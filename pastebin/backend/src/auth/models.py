from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Boolean, Column, Index, Integer, String

from database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """User model for authentication and authorization."""

    __tablename__ = 'users'

    id: int = Column(
        Integer,
        primary_key=True,
        index=True,
    )
    email: str = Column(
        String,
        nullable=False,
        unique=True,
        index=True,
    )
    username: str = Column(
        String,
        nullable=False,
        unique=True,
        index=True,
    )
    hashed_password: str = Column(
        String(length=1024),
        nullable=False,
    )
    is_active: bool = Column(
        Boolean,
        default=True,
        nullable=False,
    )
    is_superuser: bool = Column(
        Boolean,
        default=False,
        nullable=False,
    )
    is_verified: bool = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    # Indexes for frequently used columns
    __table_args__ = (
        Index('idx_users_email', email),
        Index('idx_users_username', username),
    )
