from fastapi import APIRouter
from app.f5_related.related_vs import router as vs_router
from app.f5_related.related_pool import router as pool_router
from app.f5_related.related_rules import router as rule_router

api_router = APIRouter()
api_router.include_router(vs_router, prefix="/vs", tags=['vs'])
api_router.include_router(pool_router, prefix="/pools", tags=['pools'])
api_router.include_router(rule_router, prefix="/rule", tags=['rule'])