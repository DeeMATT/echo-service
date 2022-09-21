from echo_service.core.helpers.cache.base import BaseBackend

from starlette.types import ASGIApp, Receive, Scope, Send


def blocked() -> ASGIApp:
    async def request_limit_error(scope: Scope, receive: Receive, send: Send) -> None:
        await send({"type": "http.response.start", "status": 429})
        await send({"type": "http.response.body", "body": b"Rate Limit Exceeded", "more_body": False})

    return request_limit_error


class HTTPThrottleMiddleware:
    def __init__(self, app: ASGIApp, backend: BaseBackend) -> None:
        self.app = app
        self.backend = backend

        assert isinstance(backend, BaseBackend), f"invalid backend: {self.backend}"

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> ASGIApp:
        if scope["type"] not in ("http", "https"):             # pragma: no cover
            return await self.app(scope, receive, send)

        if 'echo' in scope['path']:
            # get current rate value from redis
            request_rate = await self.backend.get("rate_per_minute")

            # get client ip address
            client_ip = scope['client'][0]
            # check if client ip already exists
            client_rate = await self.backend.get(client_ip)

            if client_rate:
                if int(client_rate) >= int(request_rate):
                    # client request limit exhausted
                    return await blocked()(scope, receive, send)

                # increment value by 1
                await self.backend.incr(client_ip)
            else:
                # client doesn't exist, create a record
                await self.backend.set(client_ip, "1", 60)

        return await self.app(scope, receive, send)
