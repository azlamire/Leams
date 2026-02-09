from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.db_core import get_async_session
from app.models.auth import UserStreamSettings
from app.utils.decode_jwt import decode_jwt
from pydantic import BaseModel
import random
import string

router = APIRouter()


class UserIdRequest(BaseModel):
    user_id: str

# TODO: Please make this in OpenAPI or it's so ugly
@router.post("/user_stream_gen")
async def generate(
        data: UserIdRequest,
        session: AsyncSession = Depends(get_async_session)
):
    # TODO: Make it hashing
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=64)) # k = len of str
    stream_id = f"live_{random_string}"
    user_id = decode_jwt(data.user_id).get("sub")
    stream_settings = UserStreamSettings(stream_id=stream_id, user_id=user_id)
    session.add(stream_settings)
    await session.commit()
    return stream_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/user_stream_gen_first_check")
async def provide(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_async_session)
):

    user_id = decode_jwt(token).get("sub")
    user = await session.execute(select(UserStreamSettings).where(UserStreamSettings.user_id == user_id))
    return user.scalars().first().get() #type: ignore
