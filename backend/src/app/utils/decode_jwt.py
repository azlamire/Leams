import jwt

# NOTE: Maybe contain all users' stuff here?
def decode_jwt( access_token: str ):
    return jwt.decode(
        access_token.strip('"'), 
        "SECRET", 
        ["HS256"], 
        audience="fastapi-users:auth"
    )
