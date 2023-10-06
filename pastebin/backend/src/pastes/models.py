from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Text
from sqlalchemy.orm import relationship

#from auth.models import User
from database import Base


class Paste(Base):
    """Paste model for storing user pastes."""

    __tablename__ = 'pastes'

    id: int = Column(
        Integer,
        primary_key=True,
        index=True,
    )
    user_id: int = Column(
        Integer,
        ForeignKey(
            'users.id',
            ondelete='CASCADE',
        ),
        nullable=False,
        index=True,
    )
    user = relationship('User')
    title: str = Column(
        String(length=50),
        nullable=True,
    )
    content: str = Column(
        Text,  # (length=10485760)  # 10 MB limit (10 * 1024 * 1024)
        nullable=True,
    )
    format: str = Column(
        String(length=25),
        nullable=True,
    )
    expire_date: str = Column(
        String(length=3),
        nullable=True,
    )
    private: bool = Column(
        Boolean,
        default=False,
        nullable=False,
    )
