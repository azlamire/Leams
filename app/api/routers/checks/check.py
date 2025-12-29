from app.db.db_core import get_session
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.models.models import Users, IsUser, IsEmail
from sqlmodel import Session, select

router = APIRouter()


@router.post("/has_user")
async def has_user(request: IsUser, session: Session = Depends(get_session)):
    result = session.exec(
        select(Users).where(Users.username == request.nickname)
    ).first()
    validUser = result is None
    return JSONResponse(status_code=200, content={"validUser": validUser})


@router.post("/has_email")
async def has_email(request: IsEmail, session: Session = Depends(get_session)):
    result = session.exec(select(Users).where(Users.email == request.email)).first()
    if "@" not in request.email:
        return JSONResponse(status_code=401, content={"validEmail": False})
    validEmail = result is None
    return JSONResponse(status_code=200, content={"validEmail": validEmail})
