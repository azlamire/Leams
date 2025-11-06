from sqlmodel import Session, select
from db.core import engine
from models.models import Users

with Session(engine) as session:
    result = session.exec(
        select(Users).where(Users.email == "refjekfjek@gmail.com")
    ).first()
    print(result)
SECRET_KEY = open("./app/core/jwt-private.pem").read()
PUBLIC_KEY = open("./app/core/jwt-public.pem").read()
print(PUBLIC_KEY)

