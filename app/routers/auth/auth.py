from fastapi import APIRouter, Depends,Response,Request
from ...schemas import UserModel
from .token_create import current_token_name, create_refresh_token, create_access_token,validate_user_auth
from .models import TokenInfo
router = APIRouter()

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
    payload = current_token_name(request.cookies.get("refresh_token"))
    return {
        "username": payload.username,
        "email": payload.email,
    }


