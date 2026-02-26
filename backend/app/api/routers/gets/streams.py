from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db_core import get_async_session
from app.models.auth import StreamList


router = APIRouter()


@router.get("/get_list_streams")
async def publish_done(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(StreamList.stream))
    return result.scalars().all()
