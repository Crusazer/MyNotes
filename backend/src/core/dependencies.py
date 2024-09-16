from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import UserNotActiveException
from src.services.auth_service import AuthService
from src.services.note import NoteService
from src.services.tag_service import TagService
from src.services.token_service import TokenService, TokenType
from src.services.user_service import UserService
from .database.database import get_async_session
from .database.models.user import User


def get_authorization_service(
    session: AsyncSession = Depends(get_async_session),
) -> AuthService:
    return AuthService(session)


def get_token_service(
    session: AsyncSession = Depends(get_async_session),
) -> TokenService:
    return TokenService(session)


def get_user_service(
    session: AsyncSession = Depends(get_async_session),
) -> UserService:
    return UserService(session)


def get_note_service(session: AsyncSession = Depends(get_async_session)) -> NoteService:
    return NoteService(session)


def get_tag_service(session: AsyncSession = Depends(get_async_session)) -> TagService:
    return TagService(session)


async def get_current_auth_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    token_service: TokenService = Depends(get_token_service),
    user_service: UserService = Depends(get_user_service),
) -> User:
    """Get current user from jwt token and check token type."""
    payload: dict = token_service.get_current_token_payload(credentials.credentials)
    token_service.check_token_type(payload, TokenType.ACCESS)
    user: User = await user_service.get_user_from_jwt(payload=payload)
    return user


def get_current_active_user(user: User = Depends(get_current_auth_user)) -> User:
    if not user.is_active:
        raise UserNotActiveException
    return user
