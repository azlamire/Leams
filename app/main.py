from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.db_core import create_db_and_tables
from fastapi.middleware.cors import CORSMiddleware
from app.core.settings import get_links_settings
from app.models import auth
import uvicorn
from app.routers import router


links = get_links_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[links.MAIN_PAGE],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
