from app.db.db_core import Base
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship


class Testing(Base):
    __tablename__ = "testing"
    id = Column(Integer, primary_key=True, index=True)
    nickname = relationship("user", back_populates="owner")
