from datetime import timedelta

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm


from fastapi.encoders import jsonable_encoder
import requests
from user_related import schemas, models
from sqlalchemy.orm import Session
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
import json
from starlette.exceptions import HTTPException
from jose import JWTError, jwt
from database.database import SessionLocal
from fastapi import Depends, FastAPI, HTTPException, status, File, UploadFile
from user_related.userauth import get_user_username, verify_password, get_user, oauth2_scheme, create_access_token, \
    get_password_hash

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def authenticate_user(fake_db, username: str, password: str):
    user = get_user_username(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/", response_model=schemas.Token, description="表单提交username，password字段返回token")
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/add_user")
def add_user(db: Session = Depends(get_db)):
    user_info = {
        "username": "admin",
        "hashed_password": get_password_hash("secret"),
        "principals": f'["user:admin","role:admin"]'
    }
    user_info = models.User(**user_info)
    db.add(user_info)
    db.commit()
    return {
        "status": 200,
        "info": "添加成功"
    }
