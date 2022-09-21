
from fastapi import Depends, APIRouter

from .schemas import RateLimitSchema
from echo_service.core.helpers.cache import RedisBackend


rate_router = APIRouter()


@rate_router.get("/rate", response_model=RateLimitSchema, status_code=200)
async def rate_limit(backend: RedisBackend = Depends(RedisBackend)) -> None:
    request_rate = await backend.get("rate_per_minute")

    if not request_rate:
        request_rate = "No Limit configured"

    return {"rate_limit": request_rate}


@rate_router.post("/rate", response_model=RateLimitSchema, status_code=201)
async def rate_limit(rate: RateLimitSchema, backend: RedisBackend = Depends(RedisBackend)) -> None:
    rate_limit = rate.rate_limit
    await backend.set("rate_per_minute", rate_limit)

    return rate
