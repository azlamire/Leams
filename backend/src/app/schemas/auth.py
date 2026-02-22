from fastapi_users import schemas
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import uuid


class UserRead(schemas.BaseUser[uuid.UUID]):
    nickname: str

class UserCreate(schemas.BaseUserCreate):
    nickname: str

class UserUpdate(schemas.BaseUserUpdate):
    nickname: str

class Base(DeclarativeBase):
    pass

class User(SQLAlchemyBaseUserTableUUID, Base):
    nickname: Mapped[str] = mapped_column(unique = True)
