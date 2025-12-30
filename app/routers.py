from app.api.routers.gets.demo import router as demo

from app.services.chat_test import router as chat
from app.api.routers.gets.auth_social import router as oauth
from app.schemas.auth import UserCreate, UserRead, UserUpdate
from fastapi import APIRouter
from app.services.auth.jwt_fin import (
    SECRET,
    auth_backend,
    current_active_user,
    fastapi_users,
    github_oauth_client,
)

router = APIRouter()
router.include_router(demo)
router.include_router(chat)
# router.include_router(oauth)
router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
router.include_router(
    fastapi_users.get_oauth_router(github_oauth_client, auth_backend, SECRET),
    prefix="/auth/github",
    tags=["auth"],
)
