from fastapi import APIRouter

from app.api.api_v1.routers import accounts, auth

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(accounts.router)
