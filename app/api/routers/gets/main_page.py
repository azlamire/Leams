from fastapi import APIRouter, Depends, Request
from sqlmodel import Session, select
from db.db_core import get_session

# TODO: Make something with this func and Depends
from typing import Annotated
import json

router = APIRouter()


# // TODO: OpenAPI endoint must be
