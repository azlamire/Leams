import enum, datetime
from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import mapped_column, Mapped
from engine import Base

# class IpVersion(enum.Enum):
    # ipv4: Mapped[str] = mapped_column(String(15))
    # ipv6: Mapped[str] = mapped_column(String(39))

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]

class Location(Base):
    __tablename__ = "location"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    country: Mapped[str]
    town: Mapped[str | None]
    time: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    ip: Mapped[str] = mapped_column(String(39))
    os: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
