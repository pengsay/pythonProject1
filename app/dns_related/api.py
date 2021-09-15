from fastapi import APIRouter
from dns_related.related_dns import router as dns_router

api_router = APIRouter()
api_router.include_router(dns_router, prefix="/dns", tags=['dns'])