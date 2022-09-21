from typing import List

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from echo_service.api.echo import echo_router
from echo_service.api.rate_limit import rate_router

from .config import config
from .middlewares import HTTPThrottleMiddleware
from .helpers.cache import RedisBackend


def init_routers(app_: FastAPI) -> None:
    app_.include_router(echo_router)
    app_.include_router(rate_router)


def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
            HTTPThrottleMiddleware,
            backend=RedisBackend()
        )
    ]
    return middleware


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Echo-Service",
        description="HTTP-based throttling echo service",
        version="0.1.0",
        docs_url=None if config.ENV == "production" else "/docs",
        redoc_url=None if config.ENV == "production" else "/redoc",
        middleware=make_middleware(),
    )
    init_routers(app_=app_)
    return app_


app = create_app()
