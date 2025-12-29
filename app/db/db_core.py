from sqlmodel import Session, SQLModel, create_engine
from app.core.settings import get_links_settings

links = get_links_settings()

engine_url = links.SYNC_PSQL

engine = create_engine(engine_url)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
