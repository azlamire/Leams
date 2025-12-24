from contextlib import contextmanager
from datetime import timedelta, datetime, timezone
from fastapi import Depends, Request
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from models.models import Users, UserLogin
from db.core import get_session
from fastapi import status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Annotated
import jwt, os
from jwt.exceptions import InvalidTokenError
from dotenv import load_dotenv

load_dotenv("../.env")


SECRET_KEY = open(os.path.abspath(".") + "/app/jwt-private.pem").read()
PUBLIC_KEY = open(os.path.abspath(".") + "/app/jwt-public.pem").read()
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# XTODO: YOU MUST MAKE A VALIDATOR FOR EVERYTHING AND LOGGING


class TokenData(BaseModel):
    username: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


def login(request: UserLogin, session: Session = Depends(get_session)):
    username = request.user_email.strip(" ")
    plain_password = request.password.strip(" ")
    user = authenticate(username, plain_password, session)
    jsonable_format = jsonable_encoder(user)
    if user == False or user is None:
        return ""
        # raise HTTPException(
        #     status_code=status.HTTP_401_UNAUTHORIZED,
        #     detail="Incorrect username or password",
        #     headers={"WWW-Authenticate": "Bearer"},
        # )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return access_token


# @app.get("/users/me/", response_model=User)
# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_active_user)],
# ):
#     return current_user
#
#
# @app.get("/users/me/items/")
# async def read_own_items(
#     current_user: Annotated[User, Depends(get_current_active_user)],
# ):
#     return [{"item_id": "Foo", "owner": current_user.username}]
#


def verify_password(plain_password, hash_password):
    try:
        return pwd_context.verify(plain_password, hash_password)
    except:
        print(plain_password, hash_password)


# TODO: Make a validator
def get_user(username: str, session: Session):
    result = ""
    if "@" in username:
        result = session.exec(select(Users).where(Users.email == username)).first()
    else:
        result = session.exec(select(Users).where(Users.username == username)).first()
    return result if result else None


def authenticate(username: str, plain_password: str, session: Session):
    user = get_user(username, session)
    if user is None:
        return None
    print(plain_password, user.password)
    if not verify_password(plain_password, user.password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    # TODO: READ ABOUT ALGORITHMS LIEK RS256
    encoded_jwt = jwt.encode(to_encode, "secret", algorithm="HS256")
    return encoded_jwt


# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)],
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
