from fastapi import FastAPI
from f5_related.api import api_router as f5_router
from user_related.api import api_router as user_router
from user_related import models
from database.database import engine
models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(f5_router)
app.include_router(user_router)
