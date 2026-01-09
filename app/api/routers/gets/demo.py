from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from app.services.s3 import S3Client

# TODO: Make something with this func and Depends
from typing import Annotated
import json

router = APIRouter()


@router.get("/main/categories{id}")
async def get_categories(id: int):
    content = await S3Client(bucket_name="testing").get_file(
        name_file=" CategoriesPohoto/"
    )
    return content


@router.get("/main/subs{id}")
async def get_subs(id: int):
    content = await S3Client(bucket_name="testing").get_file(name_file="DemoSubs.json")
    return content


@router.get("/main/streams{id}")
async def get_streams(id: int):
    # // TODO: hardcoded link though, solve it
    with open("streams.json", "r") as testing:
        test = json.load(testing)
        try:
            print(list(test.items())[id])
            return list(test.items())[id]
        except:
            return JSONResponse(status_code=404, content={"content": ""})
