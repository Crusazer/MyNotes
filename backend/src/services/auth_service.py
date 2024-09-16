import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.models.user import User
from src.core.repositories.user_repository import UserRepository
from src.core.schemas.token import SToken
from src.core.schemas.user_schemas import SUserCreate
from src.exceptions import (
    UserNotFoundException,
    UserAuthenticationException,
    NotMatchPasswordException,
    InvalidTokenException,
)
from src.utils.auth import validate_password, hash_password
from .token_service import TokenService

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, db_session: AsyncSession):
        self._session: AsyncSession = db_session
        self._repository = UserRepository(self._session)
        self._token_service = TokenService(self._session)

    def _generate_tokens(self, user: User) -> SToken:
        access_token: str = self._token_service.create_access_token(user)
        refresh_token: str = self._token_service.create_refresh_token(user)
        return SToken(access_token=access_token, refresh_token=refresh_token)

    async def login(self, email: str, password: str) -> SToken:
        """Check password and authenticate user"""
        user = await self._repository.get_user_by_email(email=email)
        if not user:
            logger.info(f"Failed login attempt by %s. User not found.", email)
            raise UserNotFoundException

        if not validate_password(password, user.password):
            logger.info(f"Failed login attempt by %s. Password didn't match.", email)
            raise UserAuthenticationException

        return self._generate_tokens(user)

    async def logout(self, refresh_token: str) -> None:
        """Logout user and add refresh token to blacklist"""
        payload = self._token_service.get_current_token_payload(refresh_token)
        await self._token_service.add_token_to_blacklist(payload)

    async def refresh_jwt_token(self, refresh_token: str, user: User) -> SToken:
        """Generate new pair and add old refresh to blacklist. If token is expired or blacklisted raise exception"""
        payload = self._token_service.get_current_token_payload(refresh_token)

        if await self._token_service.is_token_in_blacklist(payload.get("jti")):
            raise InvalidTokenException

        await self._token_service.add_token_to_blacklist(payload)
        return self._generate_tokens(user)

    async def register_user(self, email: str, password: str, re_password: str):
        """Create new user if not exists and passwords match"""
        if password != re_password:
            logger.info(f"Failed register attempt %s. User already exists.", email)
            raise NotMatchPasswordException

        hashed_password = hash_password(password)
        s_user = SUserCreate(email=email, password=hashed_password)

        if await self._repository.get_user_by_email(email=s_user.email) is not None:
            logger.info(f"User already exists: %s", s_user.email)
            raise UserAuthenticationException(
                detail="A user with this email already exists."
            )

        user = await self._repository.create_user(s_user)
        return self._generate_tokens(user)
