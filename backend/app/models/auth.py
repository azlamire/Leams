from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy.orm import relationship
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase

from app.db.db_core import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass


class StreamList(Base):
    __tablename__ = "streams"
    id = Column(Integer, primary_key=True)
    stream = Column(String, nullable=False)
    date = Column(Date, nullable=False)  # required field!

class UserStreamSettings(Base):
    __tablename__ = "user_stream_settings"
    user_id: Mapped[str] = mapped_column(ForeignKey('user.id'), primary_key=True)
    stream_id: Mapped[str]
    user = relationship("User")

# class ChatMessages(Base):
#     __tablename__ = "messages"
#     id = Column(Integer, primary_key=True, index=True)
#     nickname = relationship("user", back_populates="owner")
#     date = Column(Date, default=True)
#     stream = Column(String, default=False)
#
#
# class Moderators(Base):
#     __tablename__ = "moderators"
#     id = Column(Integer, primary_key=True, index=True)
#     nickname = relationship("users", back_populates="owner")
#     peered_to = Column(String, default=False)
