from sqlalchemy import Integer, Table, Column, String, LargeBinary, ForeignKey, Text
from sqlalchemy.orm import declarative_base

from .users import metadata, User

Base = declarative_base(metadata=metadata)

profile = Table(
    "profiles",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("text", Text, nullable=True),
    Column("image", LargeBinary, nullable=True),
    Column("banner", LargeBinary, nullable=True),
    Column("pronoun", String, nullable=True)
)


class Profile(Base):
    __table__ = profile

    @classmethod
    def create(cls, session, name: str, email: str, bio: str) -> "Profile":
        profile = cls(name=name, email=email, bio=bio)
        session.add(profile)
        session.commit()
        session.refresh(profile)
        return profile

    def update(self, session, name: str, email: str, bio: str) -> "Profile":
        self.name = name
        self.email = email
        self.bio = bio
        session.commit()
        session.refresh(self)
        return self
