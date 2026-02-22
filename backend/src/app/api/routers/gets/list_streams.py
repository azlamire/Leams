from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from fastapi.responses import JSONResponse
from app.db.db_core import get_async_session
from app.models.auth import UserStreamSettings
from app.utils.decode_jwt import decode_jwt
from pydantic import BaseModel
import random
import string

router = APIRouter()


@router.patch("/main/get_list_streams")
async def get_list_streams(
        session: AsyncSession = Depends(get_async_session)
):
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=64)) # k = len of str
    my_stream_id = f"live_{random_string}"
    user_id = decode_jwt(data.user_id).get("sub")
    stream_settings = update(UserStreamSettings).where(UserStreamSettings.user_id == user_id).values(stream_id=my_stream_id)
    await session.execute(stream_settings)
    await session.commit()
    return my_stream_id


