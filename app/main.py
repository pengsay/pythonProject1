from fastapi import FastAPI
from f5_related.api import api_router as f5_router
from user_related.api import api_router as user_router
from dns_related.api import api_router as dns_router
from firewall_related.api import api_router as firewall_router
from user_related import models
from database.database import engine
from config import Setting
from functools import lru_cache

# models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(f5_router, prefix="/f5")
app.include_router(user_router, prefix="/user")
app.include_router(dns_router, prefix="/dns")
app.include_router(firewall_router, prefix="/fw")


@lru_cache()
def get_settings():
    return Setting()
