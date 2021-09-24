from fastapi import APIRouter
# from f5_related.related_vs import router as vs_router
from firewall_related.related_pan_os import router as pan_router

api_router = APIRouter()
api_router.include_router(pan_router, prefix="/pan", tags=['pan'])
# api_router.include_router(pool_router, prefix="/pools", tags=['pools'])
# api_router.include_router(rule_router, prefix="/rule", tags=['rule'])