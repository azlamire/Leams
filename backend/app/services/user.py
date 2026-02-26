from fastapi import APIRouter, Request, status, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt, os
from pydantic import BaseModel
from typing import Annotated
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session, select
from db.core import get_session

SECRET_KEY = open(os.path.abspath(".") + "./jwt-private.pem", "r").read()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
router = APIRouter()


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        if isinstance(token, str):
            payload = jwt.decode(token, SECRET_KEY, algorithms="HS256")
            print(token, "\n", payload)
    except InvalidTokenError:
        raise credentials_exception


@router.get("/main/nav/user", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    session.exec()
