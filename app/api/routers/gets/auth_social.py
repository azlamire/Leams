from fastapi import APIRouter
from services.auth.oauth import generate_github, generate_apple

router = APIRouter()


@router.get("/auth/github")
def get_github():
    """
    Ручка которая при нажатии в окне регистрации или логина перенаправляла
    вас на вход с помощью GitHub
    """
    uri = generate_github()
    return uri


@router.get("/auth/apple")
def get_apple():
    """
    Ручка которая при нажатии в окне регистрации или логина перенаправляла
    вас на вход с помощью GitHub
    """
    uri = generate_apple()
    return uri
