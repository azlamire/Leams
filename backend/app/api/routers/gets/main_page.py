from fastapi import APIRouter, Depends, Request
from app.db.db_core import get_async_session

from app.schemas.auth import User, UserRead
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# TODO: Make something with this func and Depends
from typing import Annotated
import json, jwt

router = APIRouter()


@router.post("/main/user_info")
async def get_user_info(
    access_token: str, session: AsyncSession = Depends(get_async_session)
):
    print("TOKEN:", repr(access_token))
    decoded_one = jwt.decode(
        access_token.strip('"'), "SECRET", ["HS256"], audience="fastapi-users:auth"
    )["sub"]
    result = await session.execute(select(User).where(User.id == decoded_one))
    return dict(UserRead.model_validate(result.scalars().first())).get("email")
