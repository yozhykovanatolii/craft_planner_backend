from fastapi import APIRouter
from api.routers import auth, users

api_router = APIRouter()
api_router.include_router(auth.auth_router)
api_router.include_router(users.user_router)