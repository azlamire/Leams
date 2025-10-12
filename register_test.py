from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter
from database.core import get_session
from sqlmodel import Session
from fastapi import Depends
from fastapi.responses import RedirectResponse
from passlib.hash import bcrypt
from database.models import Users, UserRequest

router = APIRouter()

@router.post("/register")
async def register(request: Users, session: Session = Depends(get_session)):
    password = request.password
    request.password = bcrypt.hash(password)
    session.add(request)
    session.commit()
    session.refresh(request)
    return True

