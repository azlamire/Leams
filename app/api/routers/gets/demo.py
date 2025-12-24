from fastapi import APIRouter, Depends, Request
from sqlmodel import Session, select
from services.s3 import S3Client

# TODO: Make something with this func and Depends
from typing import Annotated
import json

router = APIRouter()


# // TODO: OpenAPI endoint must be
@router.get("/main/categories{id}")
async def get_categories(id: int):
    content = await S3Client(bucket_name="testing").get_file(name_file="DemoSubs.json")
    return content
