from bcrypt import hashpw
from core.jwt_fin import login
from db.core import get_session
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from core.hash_pas import hash_password
from passlib.hash import bcrypt
from models.models import Users, UserLogin
from sqlmodel import Session


router = APIRouter()


# TODO: password validator
@router.post("/register")
async def register(request: Users, session: Session = Depends(get_session)):
    plain_password = request.password
    # request.password = hash_password(request.password)
    request.password = bcrypt.hash(request.password)
    session.add(request)
    session.commit()
    session.refresh(request)
    token = login(
        UserLogin(user_email=request.username, password=plain_password),
        session=session,
    )
    return token
