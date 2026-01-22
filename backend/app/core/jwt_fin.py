from contextlib import contextmanager
from datetime import timedelta, datetime, timezone
from fastapi import Depends
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

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
PUBLIC_KEY = open("./app/core/jwt-public.pem").read()
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
        return JSONResponse(status_code=401, content={"content": jsonable_format})
        # raise HTTPException(
        #     status_code=status.HTTP_401_UNAUTHORIZED,
        #     detail="Incorrect username or password",
        #     headers={"WWW-Authenticate": "Bearer"},
        # )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return JSONResponse(status_code=200, content={"content": access_token})


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


# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, PRIVATE_KEY, algorithms=[ALGORITHM])
#         username = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except InvalidTokenError:
#         raise credentials_exception
#     user = get_user(username=token_data.username)
#     if user is False:
#         raise credentials_exception
#     return user
#
#
# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)],
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
#
