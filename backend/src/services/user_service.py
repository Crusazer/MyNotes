from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.models.user import User
from src.core.repositories.user_repository import UserRepository
from src.exceptions import UserNotFoundException
from src.services.token_service import TokenService, TokenType


class UserService:
    def __init__(self, db_session: AsyncSession):
        self._session: AsyncSession = db_session
        self._repository = UserRepository(self._session)

    async def get_user_from_jwt(self, payload: dict) -> User:
        """Get user from JWT via payload"""
        user: User | None = await self._repository.get_user_by_id(
            user_uuid=payload["sub"]
        )

        if user is None:
            raise UserNotFoundException

        return user

    async def get_current_user_for_refresh(
        self,
        refresh_token: str,
        token_service: TokenService,
    ) -> User:
        """Get current user from jwt refresh token and check token type."""
        payload: dict = token_service.get_current_token_payload(refresh_token)
        token_service.check_token_type(payload, TokenType.REFRESH)
        user: User = await self.get_user_from_jwt(payload=payload)
        return user
