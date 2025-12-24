from core.settings import git_settings
import urllib.parse
from fastapi import APIRouter

router = APIRouter()


def generate_github():
    query_params = {
        "client_id": git_settings.GITHUB_ID,
        "redirect_uri": "http://localhost:3000",
        "response_type": "code",
        "scope": "user:email",
    }
    query_strings = urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)
    base_url = "https://github.com/login/oauth/authorize"
    return f"{base_url}?{query_strings}"


def generate_apple():
    pass
