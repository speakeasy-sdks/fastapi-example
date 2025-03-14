from fastapi import APIRouter
from app.api.clerk.clerk import router as clerk_router
api_router = APIRouter()

api_router.include_router(clerk_router, tags=["Clerk"])