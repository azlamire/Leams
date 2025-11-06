"""
.. note::
   Это основной модуль проекта.

.. todo::
   Добавить обработку ошибок при вводе данных.
"""

from api.routers.checks import check
from core import register_test, oauth

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.core import create_db_and_tables
from schemas.settings import links
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[links.MAIN_PAGE],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(register_test.router)
app.include_router(oauth.router)
app.include_router(check.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
