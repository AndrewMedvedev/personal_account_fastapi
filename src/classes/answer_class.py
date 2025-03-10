from fastapi import Response
from fastapi.responses import JSONResponse

from src.classes.send_data_class import SendData
from src.classes.tokens_classes import ValidTokens
from src.interfaces import AnswerBase


class Answer(AnswerBase):

    def __init__(
        self,
        message: str,
        token_access: str,
        token_refresh: str,
    ) -> None:
        self.message = message
        self.token_access = token_access
        self.token_refresh = token_refresh
        self.response = Response
        self.valid_tokens = ValidTokens
        self.send_data = SendData()

    async def get_answer(self) -> dict:
        check_tokens = await self.valid_tokens(
            token_access=self.token_access,
            token_refresh=self.token_refresh,
        ).valid()
        data = await self.send_data.send_message_bot(self.message)
        if "access" in check_tokens:
            self.response.set_cookie(
                key="access",
                value=check_tokens.get("access"),
                samesite="none",
                httponly=True,
                secure=True,
            )
        return JSONResponse(content=data)
