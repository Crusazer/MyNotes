import logging
import uuid

from sqlalchemy import Select, select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.models.token_blacklist import TokenBlacklist

logger = logging.getLogger(__name__)


class TokenRepository:
    def __init__(self, db_session: AsyncSession):
        self._db_session = db_session

    async def add_token_to_blacklist(self, token_jti: uuid) -> None:
        """ Adds a token to the blacklist """
        token: TokenBlacklist = TokenBlacklist(jti=token_jti)
        self._db_session.add(token)
        await self._db_session.commit()

    async def get_token_by_jti(self, token_jti: uuid) -> TokenBlacklist | None:
        """ Retrieves a token from the blacklist """
        stmt: Select = select(TokenBlacklist).where(TokenBlacklist.jti == token_jti)
        result: Result = await self._db_session.execute(stmt)
        return result.scalars().first()
