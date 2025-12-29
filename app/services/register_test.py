from bcrypt import hashpw
from app.services.auth.jwt_fin import login
from app.db.db_core import get_session
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.utils.hash_pas import hash_password
from passlib.hash import bcrypt
from app.models.models import Users, UserLogin
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
    if token == "":
        return JSONResponse(status_code=401, content={"content": "error"})
    response = JSONResponse(
        status_code=200, content={"content": "Come to the dark side, we have cookies"}
    )
    response.set_cookie(key="auth_token", value=token)
    return response
