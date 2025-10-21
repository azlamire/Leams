"""
.. note::
   Это основной модуль проекта.

.. todo::
   Добавить обработку ошибок при вводе данных.
"""

from contextlib import asynccontextmanager
from core import register_test, oauth
from db.core import create_db_and_tables
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
