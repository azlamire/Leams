from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase

from app.db.db_core import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass
