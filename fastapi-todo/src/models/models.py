from sqlalchemy import Column, Integer, String

from db import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    text = Column(String, nullable=False)
