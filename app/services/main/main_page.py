from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from db.core import get_session

# TODO: Make something with this func and Depends
from typing import Annotated
import json

router = APIRouter()


# // TODO: OpenAPI endoint must be
@router.get("/main/streams{id}")
async def get_categories(id: int):
    # // TODO: hardcoded link though, solve it
    with open("app/main.json", "r") as testing:
        test = json.load(testing)
        try:
            return list(test.items())[id]
        except:
            return JSONResponse(status_code=404, content={"content": "fuck you"})
