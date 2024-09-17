import logging

import httpx
from httpx import Response

from src.config import settings
from src.database.database import User

logger = logging.getLogger(__name__)


class ApiManager:
    register_user_url = settings.API_DOMAIN + "/v1/auth/register/"

    async def register_user(self, email: str, password: str, telegram_id: int) -> User | dict | None:
        body: dict = {"email": email, "password": password, "re_password": password}
        try:
            async with httpx.AsyncClient() as client:
                response: Response = await client.post(
                    url=self.register_user_url,
                    json=body
                )
                logger.debug(response.text)
            data: dict = response.json()

            if response.status_code == 201:
                user = User(
                    email=email,
                    access_token=data['access_token'],
                    refresh_token=data['refresh_token'],
                    telegram_id=telegram_id)
                logger.info(f"Registered user: {user.email}")
                return user
            else:
                logger.error(f"Failed to register user: %s. Status code: %s. Response: %s",
                             email, response.status_code, response.text)
                return response.json()

        except Exception as e:
            logger.error(f"Failed to register user: %s", email, exc_info=e)
            return None

