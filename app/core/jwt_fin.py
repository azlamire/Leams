from contextlib import contextmanager
from datetime import timedelta, datetime, timezone
from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from models.models import Users, UserLogin
from main import app
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

SECRET_KEY = open("jwt-private.pem").read()
PUBLIC_KEY = open("jwt-public.pem").read()
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "RS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class TokenData(BaseModel):
    username: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


@app.post("/token")
def login(request: UserLogin, session: Session = Depends(get_session)):
    username = request.user_email.strip(" ")
    plain_password = request.password.strip(" ")
    user = authenticate(username, plain_password, session)
    jsonable_format = jsonable_encoder(user)
    if user == False:
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
    return Token(access_token=access_token, token_type="bearer")


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
    return pwd_context.verify(plain_password, hash_password)


def get_user(username: str, session: Session) -> dict | None:
    if "@" in username:
        result = session.exec(select(Users).where(Users.email == username)).first()
    else:
        result = session.exec(select(Users).where(Users.username == username)).first()
    return result


def authenticate(username: str, plain_password: str, session: Session):
    user = get_user(username, session)
    if user is None:
        return False
    if not verify_password(plain_password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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
