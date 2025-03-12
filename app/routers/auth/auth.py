from fastapi import APIRouter, Depends,Response,Request
from ...schemas import UserModel
from sqlalchemy.ext.asyncio import async_sessionmaker
from ...db.database import engine
from .token_create import current_token_name, create_refresh_token, create_access_token,validate_user_auth
from .models import TokenInfo
from ...db.orm import UsersCRUD
from .utils import hash_password

router = APIRouter()

users_crud = UsersCRUD()
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

@router.post("/token/",response_model=TokenInfo)
async def auth(
        response: Response,
        user: UserModel = Depends(validate_user_auth)
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    response.set_cookie(
        key="refresh_token",
        value = refresh_token,
        httponly=True,
        samesite="strict",
        secure=True,
        max_age=7*24*60*60
    )
    return TokenInfo(
        access_token = access_token,
        refresh_token = refresh_token,
    )

@router.get("/auth/me")
async def auth_me(
        request:Request,
):
    payload = await current_token_name(request.cookies.get("refresh_token"))
    return {
        "username": payload.username,
        "email": payload.email,
    }

@router.get("/auth/logout")
async def auth_logout(request:Request):
    try:
        request.cookies.pop("refresh_token")
    finally:
        return {"User": "logout"}

@router.post("/register/")
async def auth_register(
        user: UserModel
):
    user.hashed_password = hash_password(user.hashed_password).decode("utf-8")

    await users_crud.insert_user(AsyncSessionLocal,user)
    return {"User": "register"}