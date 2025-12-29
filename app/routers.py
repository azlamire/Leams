from app.api.routers.gets.demo import router as demo
from app.services.chat_test import router as chat
from app.services.auth.jwt_fin import fastapi_users, auth_backend
from app.schemas.auth import UserCreate, UserRead, UserUpdate
from fastapi import APIRouter

router = APIRouter()
router.include_router(demo)
router.include_router(chat)
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
