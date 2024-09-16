import enum
import logging
import typing
import uuid

from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.core.database.models.user import User
from src.core.repositories.token_repository import TokenRepository
from src.exceptions import (
    InvalidTokenException,
    InvalidTokenTypeException,
)
from src.utils.auth import encode_jwt, decode_jwt

if typing.TYPE_CHECKING:
    from src.core.database.models.token_blacklist import TokenBlacklist

logger = logging.getLogger(__name__)


class TokenType(enum.StrEnum):
    TYPE = "type"
    ACCESS = "access"
    REFRESH = "refresh"


class TokenService:

    def __init__(self, db_session: AsyncSession):
        self._session: AsyncSession = db_session
        self._repository: TokenRepository = TokenRepository(db_session)

    async def add_token_to_blacklist(self, payload: dict) -> None:
        """Add refresh token to blacklist"""
        jti = payload.get("jti")
        await self._repository.add_token_to_blacklist(jti)
        logger.info(f"Added token %s to blacklist", jti)

    async def is_token_in_blacklist(self, jti: uuid) -> bool:
        """ Return true if token founded in black list. """
        token: TokenBlacklist | None = await self._repository.get_token_by_jti(jti)
        logger.info(f"Check token: %s in blacklist. Token is %s", jti, token)
        return bool(token)

    def create_access_token(self, user: User) -> str:
        jwt_payload = {"sub": str(user.id)}
        return self._create_jwt_token(
            jwt_payload, TokenType.ACCESS, settings.ACCESS_TOKEN_LIFE
        )

    def create_refresh_token(self, user: User) -> str:
        jwt_payload = {"sub": str(user.id), "jti": str(uuid.uuid4())}
        return self._create_jwt_token(
            jwt_payload, TokenType.REFRESH, settings.REFRESH_TOKEN_LIFE
        )

    @staticmethod
    def _create_jwt_token(
            payload: dict, token_type: TokenType, expire_time_minutes: int
    ) -> str:
        payload[TokenType.TYPE.value] = token_type.value
        return encode_jwt(payload, expire_minutes=expire_time_minutes)

    @staticmethod
    def get_current_token_payload(token: str) -> dict:
        try:
            payload: dict = decode_jwt(token=token)
        except InvalidTokenError as e:
            logger.info(f"Invalid token: %s", token)
            raise InvalidTokenException
        return payload

    @staticmethod
    def check_token_type(payload: dict, token_type: TokenType) -> None:
        current_type_type = payload.get(TokenType.TYPE)
        if current_type_type != token_type:
            logger.error(f"Invalid token: %s", token_type)
            raise InvalidTokenTypeException(
                detail=f"Invalid token type {current_type_type!r}. Expected {token_type.value!r}"
            )
