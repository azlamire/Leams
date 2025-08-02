from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt
import uvicorn, os

def main():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
    )
    jwt_secret = os.getenv("SECRET")
    token = jwt.encode({},jwt_secret)
    print(token)
    response = Response()
    response.set_cookie(ket="access_token", value=token,httponly=True)

if __name__ == "__main__":
    uvicorn.run(main())
