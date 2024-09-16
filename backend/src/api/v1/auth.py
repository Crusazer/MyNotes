from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.params import Body
from pydantic import EmailStr
from starlette.responses import JSONResponse

from src.core.database.models.user import User
from src.core.dependencies import (
    get_authorization_service,
    get_current_active_user,
    get_token_service,
    get_user_service
)
from src.core.schemas.token import SToken
from src.services.auth_service import AuthService
from src.services.user_service import UserService

router = APIRouter(prefix="/v1/auth", tags=["auth"])


@router.post("/login/", response_model=SToken)
async def login_user(
        email: Annotated[EmailStr, Body()],
        password: Annotated[str, Body()],
        auth_service: AuthService = Depends(get_authorization_service),
):
    return await auth_service.login(email, password)


@router.post("/logout/")
async def logout(
        refresh_token: Annotated[str, Body()],
        user: User = Depends(get_current_active_user),
        auth_service: AuthService = Depends(get_authorization_service),
):
    await auth_service.logout(refresh_token)
    return JSONResponse({"message": "Successfully logged out"})


@router.post("/refresh_token/", response_model=SToken)
async def refresh_jwt_token(
        refresh_token: Annotated[str, Body()],
        auth_service: AuthService = Depends(get_authorization_service),
        user_service: UserService = Depends(get_user_service),
        token_service=Depends(get_token_service),
) -> SToken:
    user: User = await user_service.get_current_user_for_refresh(refresh_token, token_service)
    return await auth_service.refresh_jwt_token(refresh_token, user)


@router.post("/register/", response_model=SToken, status_code=201)
async def create_user(
        email: Annotated[EmailStr, Body()],
        password: Annotated[str, Body()],
        re_password: Annotated[str, Body()],
        auth_service: AuthService = Depends(get_authorization_service),
) -> SToken:
    return await auth_service.register_user(email, password, re_password)
