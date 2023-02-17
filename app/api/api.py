from fastapi import APIRouter
from app.api.routers import auth, profile


api_router = APIRouter()


api_router.include_router(auth.router)
api_router.include_router(profile.router)
