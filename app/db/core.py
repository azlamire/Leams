from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select, table

from dotenv import load_dotenv
import os

load_dotenv(".env")
engine_url = os.getenv("SYNC_PSQL")

engine = create_engine(engine_url)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
