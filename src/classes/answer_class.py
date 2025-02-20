from fastapi import Response, status
from fastapi.responses import JSONResponse

from src.classes.send_data_class import SendData
from src.classes.tokens_classes import ValidTokens


class Answer:

    def __init__(
        self,
        message: str,
        token_access: str,
        token_refresh: str,
        response: Response,
    ) -> None:
        self.message = message
        self.token_access = token_access
        self.token_refresh = token_refresh
        self.response = response

    async def answer(self) -> dict:
        check_tokens = await ValidTokens(
            token_access=self.token_access,
            token_refresh=self.token_refresh,
            response=self.response,
        ).valid()
        match check_tokens:
            case True:
                data = await SendData.send_message_bot(self.message)
                return JSONResponse(content=data)
            case False:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                )
            case _:
                data = await SendData.send_message_bot(self.message)
                self.response.set_cookie(
                    key="access",
                    value=check_tokens.get("access"),
                    samesite="none",
                    httponly=True,
                    secure=True,
                )
                return JSONResponse(content={"answer": data})
