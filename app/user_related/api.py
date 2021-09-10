from fastapi import APIRouter
from user_related.get_token import router as token_router
api_router = APIRouter()
api_router.include_router(token_router, prefix="/token", tags=['token'])