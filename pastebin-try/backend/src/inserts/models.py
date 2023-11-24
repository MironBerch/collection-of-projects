from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Paste(Base):
    """Model for blocks of text."""

    __tablename__ = 'pastes'

    id = Column(
        Integer,
        primary_key=True,
    )
    user_id = Column(
        Integer,
        ForeignKey('users.id'),
        index=True,
    )
    title = Column(String(50))
    description = Column(String(500))
    link_to_text = Column(String)

    user = relationship(
        'User',
        backref='pastes',
        lazy='joined',
    )
