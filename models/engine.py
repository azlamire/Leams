from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv
import os


load_dotenv("../.env")
engine_url = os.getenv("SYNC_PSQL")
if not engine_url:
    raise ValueError("SYNC_PSQL environment variable is not set")

engine = create_engine(
    engine_url,
    echo=True,
    pool_size=5,
)
if not engine:
    raise ValueError("No engine was found")

session_factory = sessionmaker(bind=engine)
class Base(DeclarativeBase):
    pass
