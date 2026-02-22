from fastapi import APIRouter, WebSocket
from app.db.db_core import get_async_session

router = APIRouter()


@router.websocket("/video/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
