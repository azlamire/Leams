from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, Response, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, EmailStr
from datetime import datetime

from sqlmodel import Session, select
from database.models import IsUser, Users, UserCreate
from database.smod import create_db_and_tables, get_session
import uvicorn, os

from passlib.context import CryptContext
from contextlib import asynccontextmanager

SECRET_KEY = open("jwt-private.pem").read()
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(lifespan=lifespan)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password)
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)



def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Add this
    allow_headers=["*"]
)

#------------------------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"conent" : request, "message" : "LOOOOOOOOOOOOOOOOOOOOOOOOX"}
    )
class RequestCreateUser(BaseModel):
    username: str
    password: str
    email: EmailStr
    birthday: str


@app.post("/has_user")
async def has_user(user: IsUser , session: Session = Depends(get_session)):
    result = session.exec(select(Users).where(Users.username == user.nickname)).first()
    validUser = result is not None
    return {"invalidUser": validUser }


    
@app.get("has_email")
async def has_email():
    pass

@app.post("/register")
async def register(request: UserCreate, session: Session = Depends(get_session)):
    user = Users(**request.dict())
    session.add(user)
    session.commit()
    session.refresh(user)
    return RedirectResponse(url="http://localhost:3000",status_code=303)

#------------------------------
@app.post("/auth/")
def authentication(request):
    return {"SDDSD": "SSDKAKDKAS"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
