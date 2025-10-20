from oauth_model import settings
import urllib.parse
from fastapi import APIRouter
from dotenv import load_dotenv
import os

router = APIRouter()

def generate():
    query_params = {
        "client_id": settings.GITHUB_ID,
        "redirect_uri" : "http://localhost:3000",
        "response_type" : "code",
        "scope" : ["read:user","user:email"],
    }
    query_strings = urllib.parse.urlencode(query_params,quote_via=urllib.parse.quote)
    base_url="https://github.com/login/oauth/authorize"
    return f"{base_url}?{query_strings}"


@router.get("/auth/github")
def get_google():
    """
        Ручка которая при нажатии в окне регистрации или логина перенаправляла
        вас на вход с помощью GitHub
    """
    uri = generate()
    return uri

