from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Text, Boolean, JSON, DateTime, ForeignKey, MetaData
from enum import Enum

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(60), nullable=False)
    email = Column(String(60), nullable=False, unique=True)
    password = Column(String(16), nullable=False)
    emailsec = Column(String(60))
    record = Column(DateTime(), nullable=False)
    note = relationship("NoteModel")

    def __repr__(self):
        return f"<User id: {self.id} email: {self.email}>"


class NoteModel(Base):
    __tablename__ = "note"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    text = Column(Text(1000), nullable=True)
    record = Column(DateTime(), nullable=False)
    modified = Column(DateTime(), nullable=False)
    favorite = Column(Boolean(False))
    tags = Column(JSON())
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("UserModel", back_populates="note")

    def __repr__(self):
        return f"<Note id: {self.id} title: {self.title}>"


class UserConfig(Enum):
    NAME = "name"
    EMAIL = "email"
    PASSWORD = "password"
    EMAILSEC = "emailsec"


class NoteConfig(Enum):
    TITLE = "title"
    TEXT = "text"
    RECORD = "record"
    FAVORITE = "favorite"
    TAGS = "tags"
    USER_ID = "user_id"
    MODIFIED = "modified"


if __name__ == "__main__":
    Base.metadata.create_all()

