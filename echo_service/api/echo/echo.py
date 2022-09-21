
from fastapi import APIRouter

echo_router = APIRouter()


@echo_router.post("/echo", status_code=200)
async def echo(body: dict):
    return body
