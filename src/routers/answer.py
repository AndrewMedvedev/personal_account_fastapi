from fastapi import APIRouter, Request

from src.classes import Answer
from src.responses import CustomResponse

router_answer = APIRouter(prefix="/api/v1/answer", tags=["answer"])


@router_answer.get(
    "/{message}",
    response_model=None,
)
async def answer(
    message: str,
    request: Request,
) -> CustomResponse:
    return await Answer().get_answer(
        message=message,
    )
