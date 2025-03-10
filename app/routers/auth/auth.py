import datetime
from datetime import timedelta
from fastapi import APIRouter, Form, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from pydantic import BaseModel
from .utils import *
from ...schemas import UserModel
router = APIRouter()

den = UserModel(
    username="den",
    email="den@den.com",
    password=hash_password("password")
)
floyse = UserModel(
    username="floyse",
    email="floyse@floyse.com",
    password=hash_password("mypassword")
)

oath_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

users_db = {
    den.username: den,
    floyse.username: floyse
}

class TokenInfo(BaseModel):
    access_token: str
    token_type: str

def validate_user_auth(username:str=Form(),
                       password:str=Form()
                       ):
    uniq_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    if not (user:= users_db.get(username.strip())):
        raise uniq_exc

    if not verify_password(password,user.password):
        raise uniq_exc
    return user

@router.post("/token/",response_model=TokenInfo)
async def auth(
        user: UserModel = Depends(validate_user_auth)
):
    jwt_payload = {
        "sub": user.username,
        "email": user.email,
        "exp": datetime.datetime.utcnow() + timedelta(minutes=15)
    }
    token = encode_jwt(payload=jwt_payload)
    return TokenInfo(
        access_token = token,
        token_type = "Bearer"
    )


def current_token_name(
        token = Depends(oath_scheme)
):
    payload = decode_jwt(token)

    if (user := users_db.get(payload.get("sub"))) is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    return user

@router.get("/auth/me")
async def auth_me(
        payload = Depends(current_token_name)
):
    return {
        "username": payload.username,
        "email": payload.email,
    }


