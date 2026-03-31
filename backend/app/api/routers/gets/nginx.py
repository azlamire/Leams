from fastapi import APIRouter, Depends, Form
from fastapi.responses import JSONResponse
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db_core import get_async_session
from app.models.auth import StreamList


# TODO: Make something with this func and Depends

router = APIRouter()


@router.post("/stream_creation")
async def on_publish(
    app: str = Form(...),
    name: str = Form(...),
    tcurl: str = Form(None),
    addr: str = Form(None),
    session: AsyncSession = Depends(get_async_session),
):
    return JSONResponse("OK", status_code=200)


@router.post("/stream_ending")
async def publish_done(
    app: str = Form(...),
    name: str = Form(...),
    tcurl: str = Form(None),
    addr: str = Form(None),
    session: AsyncSession = Depends(get_async_session),
):
    stmt = delete(StreamList).where(StreamList.stream == name)
    await session.execute(stmt)
    await session.commit()
