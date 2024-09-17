import logging
import uuid

import httpx
from httpx import Response

from src.config import settings
from src.database import database as db
from src.database.database import User

logger = logging.getLogger(__name__)


class ApiManager:
    register_user_url = settings.API_DOMAIN + "/v1/auth/register/"
    refresh_token_url = settings.API_DOMAIN + "/v1/auth/refresh_token/"
    get_all_notes_url = settings.API_DOMAIN + "/v1/notes/all/"
    get_note_url = settings.API_DOMAIN + "/v1/notes/"
    create_note_url = settings.API_DOMAIN + "/v1/notes/create/"
    delete_notes_url = settings.API_DOMAIN + "/v1/notes/delete/"
    edit_note_url = settings.API_DOMAIN + "/v1/notes/update/"

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
            elif response.status_code == 403:
                logger.error(f"Failed to register user: %s. Status code: %s. Response: %s",
                             email, response.status_code, response.text)
                return "Пользователь с таким email уже зарегистрирован."
            elif response.status_code == 422:
                logger.error(f"Failed to register user: %s. Status code: %s. Response: %s",
                             email, response.status_code, response.text)
                return "Неверный email."

        except Exception as e:
            logger.error(f"Failed to register user: %s", email, exc_info=e)
            return None

    async def get_note_by_uuid(self, user: User, note_uuid: uuid.UUID) -> dict | str:
        """ Return dict with note or string with text for answer """
        try:
            async with httpx.AsyncClient() as client:
                response: Response = await client.get(
                    url=f"{self.get_note_url}{note_uuid}/",
                    headers={"Authorization": f"Bearer {user.access_token}"}
                )

                if response.status_code == 401:
                    await self.refresh_token(user)
                    response: Response = await client.get(
                        url=f"{self.get_note_url}{note_uuid}/",
                        headers={"Authorization": f"Bearer {user.access_token}"}
                    )

                if response.status_code == 200:
                    return response.json()

                if response.status_code == 404:
                    return "Заметка не найдена."
                else:
                    logger.error(f"Failed to get note for user: %s. Status code: %s. Response: %s",
                                 user.email, response.status_code, response.text)
                    return "Неудалось получить заметку. Попробуйте повторить позже."
        except Exception as e:
            logger.error(f"Failed to get note for user: %s. Response: %s",
                         user.email, response.text, exc_info=e)

    async def get_all_user_notes(self, user: User) -> list[dict]:
        try:
            async with httpx.AsyncClient() as client:
                response: Response = await client.get(
                    url=self.get_all_notes_url,
                    headers={"Authorization": f"Bearer {user.access_token}"})

                # Non authorize error
                if response.status_code == 401:
                    await self.refresh_token(user)
                    response: Response = await client.post(
                        url=self.get_all_notes_url,
                        headers={"Authorization": f"Bearer {user.access_token}"})

                if response.status_code == 404:
                    return []
                elif response.status_code == 200:
                    return response.json()
                else:
                    logger.error(f"Failed to get notes for user: %s. Response: %s", user.email, response.text)

        except Exception as e:
            logger.error(f"Failed to get user notes: %s", e, exc_info=e)

    async def create_note(self, user: User, data: dict) -> str:
        """ Create new note """
        try:
            async with httpx.AsyncClient() as client:
                response: Response = await client.post(
                    url=self.create_note_url,
                    headers={"Authorization": f"Bearer {user.access_token}"},
                    json=data
                )
                # If access token deprecated than refresh and try again.
                if response.status_code == 401:
                    await self.refresh_token(user)
                    response: Response = await client.post(
                        url=self.create_note_url,
                        headers={"Authorization": f"Bearer {user.access_token}"},
                        json=data
                    )

                # Check status code and return answer
                if response.status_code == 422:
                    logger.error(f"Failed to create note: %s. Status code: %s. Response: %s",
                                 user.email, response.status_code, response.text)
                    return f"Неверные данные, попробуйте ещё раз. {response.text}"
                elif response.status_code == 201:
                    logger.info(f"Created new note: %s", user.email)
                    return "Заметка успешна создана."
                else:
                    logger.error(f"Failed to create new note: %s. Response status: %s",
                                 response.text, response.status_code)
                    return f"Что-то пошло не так. Попробуйте ещё раз позже."
        except Exception as e:
            logger.error(f"Failed to create note: %s", e, exc_info=e)

    async def edit_note(self, user: User, note_uuid: uuid.UUID, data: dict) -> str:
        try:
            async with httpx.AsyncClient() as client:
                response: Response = await client.patch(
                    url=f"{self.edit_note_url}{note_uuid}/",
                    headers={"Authorization": f"Bearer {user.access_token}"},
                    json=data
                )

                if response.status_code == 401:
                    await self.refresh_token(user)
                    response: Response = await client.patch(
                        url=f"{self.edit_note_url}{note_uuid}/",
                        headers={"Authorization": f"Bearer {user.access_token}"},
                        json=data
                    )

                if response.status_code == 404:
                    return "Заметка не найдена."

                if response.status_code == 200:
                    return "Заметка успешно изменена."

                logger.error(f"Failed to delete note for user: %s. Response: ",
                             user.email, response.text)
                return "Что-то пошло не так. Попробуйте позже."

        except Exception as e:
            logger.error(f"Failed to delete note: %s", e, exc_info=e)

    async def delete_note(self, user: User, note_id: uuid.UUID) -> str:
        try:
            async with httpx.AsyncClient() as client:
                response: Response = await client.delete(
                    url=f"{self.delete_notes_url}{note_id}/",
                    headers={"Authorization": f"Bearer {user.access_token}"}
                )

                if response.status_code == 401:
                    await self.refresh_token(user)
                    response: Response = await client.delete(
                        url=f"{self.delete_notes_url}{note_id}/",
                        headers={"Authorization": f"Bearer {user.access_token}"}
                    )

                if response.status_code == 404:
                    return "Заметка не найдена."

                if response.status_code == 202:
                    return "Заметка успешно удалена."

                logger.error(f"Failed to delete note for user: %s, note_id: %s. Response: ",
                             user.email, note_id, response.text)
                return "Что-то пошло не так. Попробуйте позже."

        except Exception as e:
            logger.error(f"Failed to delete note: %s", e, exc_info=e)

    async def refresh_token(self, user: User) -> None:
        """ Refresh JWT token. Update user object and save to database. """
        try:
            async with httpx.AsyncClient() as client:
                response: Response = await client.post(
                    url=self.refresh_token_url,
                    json=user.refresh_token
                )

                if response.status_code == 200:
                    data: dict = response.json()
                    user.access_token = data['access_token']
                    user.refresh_token = data['refresh_token']
                    await db.update_tokens(user)
                else:
                    logger.error(f"Failed to update token: %s", response.text)
        except Exception as e:
            logger.error(f"Failed to update token: %s", e, exc_info=e)
