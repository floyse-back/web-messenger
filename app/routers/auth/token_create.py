from datetime import timedelta,datetime,timezone

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,Form
from starlette import status
from .utils import *
from ...db.orm import UsersCRUD
from ...schemas import UserModel
from ...config import JWTAuthConfig
from app.db.models import Users
from sqlalchemy.ext.asyncio import async_sessionmaker
from ...db.database import engine


oath_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
jwtauth = JWTAuthConfig()

users_crud = UsersCRUD()
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


users_db = {

}

def create_refresh_token(
        user: UserModel
) -> str:
    jwt_payload = {
        "type": "refresh_token",
        "sub": user.username,
        "exp": datetime.now(
            timezone.utc) + timedelta(minutes = jwtauth.refresh_token_expire_minutes),
        "iat": datetime.now(timezone.utc)
    }
    return encode_jwt(jwt_payload)

def create_access_token(
        user: UserModel
):
    jwt_payload = {
        "type": "access_token",
        "sub": user.username,
        "email": user.email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=jwtauth.access_token_expire_minutes),
        "iat": datetime.now(timezone.utc)
    }
    return encode_jwt(jwt_payload)

def check_token_type(token:str,token_type:str="refresh_token"):
    payload = decode_jwt(token)

    if payload.get("type") != token_type:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )
    return payload

async def current_token_name(
        token = Depends(oath_scheme)
):
    payload = check_token_type(token)
    print(payload)
    if (user := await users_crud.find_user(AsyncSessionLocal,payload.get("sub"))) is None:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Could not validate credentials"
        )

    return user

async def validate_user_auth(username:str=Form(),
                       password:str=Form()
                       ):
    uniq_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    if not (user:= await users_crud.find_user(AsyncSessionLocal,username)) :
        raise uniq_exc

    if not verify_password(password,user.hashed_password):
        raise uniq_exc
    return user