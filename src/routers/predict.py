from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse

from src.classes import Predict
from src.database.schemas import PredictFree, PredictModel

router_predict = APIRouter(prefix="/api/v1/predict", tags=["predict"])


@router_predict.post(
    "/",
    response_model=None,
)
async def predict(
    model: PredictModel,
    request: Request,
    response: Response,
) -> JSONResponse:
    try:
        access = request.cookies.get("access")
        refresh = request.cookies.get("refresh")
        return await Predict(
            token_access=access,
            token_refresh=refresh,
            model=model,
            response=response,
        ).predict()
    except Exception as e:
        return JSONResponse(
            content={"detail": str(e)},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


@router_predict.get(
    "/direction/{direction_id}",
    response_model=None,
)
async def direction(
    direction_id: int,
    request: Request,
    response: Response,
) -> JSONResponse:
    try:
        access = request.cookies.get("access")
        refresh = request.cookies.get("refresh")
        return await Predict(
            token_access=access,
            token_refresh=refresh,
            response=response,
        ).get_direction(direction_id=direction_id)
    except Exception as e:
        return JSONResponse(
            content={"detail": str(e)},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


@router_predict.get(
    "/points/{direction_id}",
    response_model=None,
)
async def points(
    direction_id: int,
    request: Request,
    response: Response,
) -> JSONResponse:
    try:
        access = request.cookies.get("access")
        refresh = request.cookies.get("refresh")
        return await Predict(
            token_access=access,
            token_refresh=refresh,
            response=response,
        ).get_points(direction_id=direction_id)
    except Exception as e:
        return JSONResponse(
            content={"detail": str(e)},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


@router_predict.post(
    "/free",
    response_model=None,
)
async def predict_free(model: PredictFree) -> float | JSONResponse:
    try:
        return await Predict().predict_free(model=model)
    except Exception as e:
        return JSONResponse(
            content={"detail": str(e)},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
