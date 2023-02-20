from fastapi import APIRouter
from app.api.routers import auth, profile, search


api_router = APIRouter()


api_router.include_router(auth.router, tags=['Auth'])
api_router.include_router(profile.router, tags=['Profile'])
api_router.include_router(search.router, tags=['Search'])
