from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse

from src.classes import Answer

router_answer = APIRouter(prefix="/api/v1/answer", tags=["answer"])


@router_answer.get(
    "/{message}",
    response_model=None,
)
async def answer(
    message: str,
    request: Request,
    response: Response,
) -> JSONResponse:
    try:
        access = request.cookies.get("access")
        refresh = request.cookies.get("refresh")
        return await Answer(
            message=message,
            token_access=access,
            token_refresh=refresh,
            response=response,
        ).get_answer()
    except Exception as e:
        return JSONResponse(
            content={"detail": str(e)},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
