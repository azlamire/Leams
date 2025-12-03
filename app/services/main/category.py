from fastapi import APIRouter, Depends, Request
from sqlmodel import Session, select
from db.core import get_session

# TODO: Make something with this func and Depends
from typing import Annotated
import json

router = APIRouter()


# // TODO: OpenAPI endoint must be
@router.get("/main/categories{id}")
async def get_categories(id: int):
    # // TODO: hardcoded link though, solve it
    with open("app/category.json", "r") as testing:
        test = json.load(testing)
        return list(test.items())[id]
