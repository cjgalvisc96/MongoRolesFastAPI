
from fastapi import APIRouter

from app.api.api_v1.routers import accounts

api_router = APIRouter()
api_router.include_router(accounts.router)