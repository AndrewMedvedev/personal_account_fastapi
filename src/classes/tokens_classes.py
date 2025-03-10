import json

from aiohttp import ClientSession
from fastapi import Response

from src.config import Settings


class ValidTokens:

    def __init__(
        self,
        token_access: str,
        token_refresh: str,
    ) -> None:
        self.token_access = token_access
        self.token_refresh = token_refresh
        self.response = Response
        self.clientsession = ClientSession
        self.settings = Settings

    async def valid(self) -> dict | str:
        send_access = await self.__send_access_token(self.token_access)
        try:
            if isinstance(send_access, dict):
                return send_access
            send_refresh = await self.__send_refresh_token(self.token_refresh)
            self.response.delete_cookie(
                key="access",
                samesite="none",
                httponly=True,
                secure=True,
            )
            return send_refresh
        except Exception as e:
            return e

    async def __send_refresh_token(
        self,
        token_refresh: str,
    ) -> dict:
        async with self.clientsession() as session:
            async with session.get(
                url=f"{self.settings.VALIDATE_REFRESH}{token_refresh}",
            ) as response:
                token = await response.text()
                return json.loads(token)

    async def __send_access_token(
        self,
        token_access: str,
    ) -> dict:
        async with self.clientsession() as session:
            async with session.get(
                url=f"{self.settings.VALIDATE_ACCESS}{token_access}",
            ) as response:
                token = await response.text()
                return json.loads(token)
