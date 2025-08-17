import jwt
from models import settings
from typing import Annotated
import bcrypt

def encode_jwt(
        payload: dict,
        private_key: str =settings.auth_jwt.private_key_path.read_text(), 
        alogorithm: str =settings.auth_jwt.alogorithm,
    ):
    encoded = jwt.encode(payload,private_key,alogorithm)
    return encoded
def decoded_jwt(
        jwt: str | bytes, 
        key: str = settings.auth_jwt.public_key_path.read_text(),
        alogorithm: str = settings.auth_jwt.alogorithm):
    decoded = jwt.decode(jwt,key,alogorithm)
    return decoded

def hash_password(
        password: str, 
    ):
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes,salt=salt)

def check_password(
        password: str, 
        hashed_password: str | bytes
    ) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password
    )
