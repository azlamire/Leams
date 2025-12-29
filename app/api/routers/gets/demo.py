from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from app.services.s3 import S3Client

# TODO: Make something with this func and Depends
from typing import Annotated
import json

router = APIRouter()


@router.get("/main/categories{id}")
async def get_categories(id: int):
    content = await S3Client(bucket_name="testing").get_file(name_file="x.json")
    return content


@router.get("/main/categories{id}")
async def get_subs(id: int):
    content = await S3Client(bucket_name="testing").get_file(name_file="DemoSubs.json")
    return content
