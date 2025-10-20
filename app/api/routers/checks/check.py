from fastapi import APIRouter

router = APIRouter()


@router.post("/has_user")
async def has_user(user: IsUser, session: Session = Depends(get_session)):
    result = session.exec(select(Users).where(Users.username == user.nickname)).first()
    validUser = result is not None
    return {"invalidUser": validUser}


@router.get("has_email")
async def has_email():
    pass
