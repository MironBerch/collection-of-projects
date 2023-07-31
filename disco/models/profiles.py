from sqlalchemy import Integer, Table, Column, String, LargeBinary, ForeignKey, Text
from sqlalchemy.orm import declarative_base

from .users import metadata

Base = declarative_base(metadata=metadata)

profile = Table(
    "profiles",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("text", Text, nullable=True),
    Column("image", LargeBinary, nullable=True),
    Column("pronoun", String, nullable=True)
)


class Profile(Base):
    __table__ = profile

    @classmethod
    def create(
        cls, session, user_id: int, text: str = None, pronoun: str = None, image: bytes = None
    ) -> "Profile":
        profile = cls(text=text, user_id=user_id, pronoun=pronoun, image=image)
        session.add(profile)
        session.commit()
        session.refresh(profile)
        return profile

    def update(self, session, text: str, user_id: int, pronoun: str, image: bytes) -> "Profile":
        self.text = text
        self.user_id = user_id
        self.pronoun = pronoun
        self.image = image
        session.commit()
        session.refresh(self)
        return self
