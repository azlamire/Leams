from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from database.models import Users
from jwt_test import hash_password
from main import app
from models.jwt_schemes import User
from database.smod import get_session
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from os import getenv


SECRET_KEY = open("jwt-private.pem").read()
ALGORITHM = getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/login")
def login(request: User):
    username = request.username
    plain_password = request.password
    user = get_user(username)
    verify_password(plain_password, hash_password)

def get_user(username: str, session: Session = Depends(get_session))
    if "@" in username:
        result = session.exec(select(Users).where(Users.email == username)).first()
    else:
        result = session.exec(select(Users).where(Users.username == username)).first()
    return result if (result is None) == False else JSONResponse( 
         content={"conent": request, "message" : "Enter the username or password please", "isAccept": False},
         status_code=400
    )
def verify_password(plain_password, hash_password):
    return pwd_context.verify_password(plain_password,hash_password)
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user




    # return JSONResponse(
    #     content={"conent": request, "message" : "OK", "isAccept": True},
    #     status_code=20r
    # ) if  request.password and request.username else JSONResponse(
    #     content={"conent": request, "message" : "Enter the username or password please", "isAccept": False},
    #     status_code=400
    # ) 



@app.post("")
