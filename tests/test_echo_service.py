import pytest
from echo_service.core import app
from echo_service.core.helpers.cache import RedisBackend
from httpx import AsyncClient


@pytest.fixture
def backend() -> RedisBackend:
    """
    Fixture to setup redis backend
    """
    return RedisBackend()


@pytest.fixture
@pytest.mark.anyio
async def get_rate(backend: RedisBackend) -> str | None:
    """
    Fixed rate for testing HTTP Request Rate Limit
    """
    return await backend.get("rate_per_minute")


@pytest.fixture
@pytest.mark.anyio
async def delete_limit(backend: RedisBackend) -> None:
    """
    Teardown fixture to delete rate limit for test client `127.0.0.1` after test
    """
    yield None
    await backend.delete("127.0.0.1")


@pytest.mark.anyio
async def test_rate_limit() -> None:
    """
    Test Rate Limit API
    """
    rate_limit = "100"

    payload = {
        "rate_limit": rate_limit
    }

    # set new rate limit
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.post(
            "/rate",
            headers={"content-Type": "application/json"},
            json=payload
        )
        assert response.status_code == 201
        assert response.json() == {"rate_limit": rate_limit}

    # get current rate limit
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.get("/rate")

        assert response.status_code == 200
        assert response.json() == {"rate_limit": rate_limit}


@pytest.mark.anyio
async def test_echo(get_rate: str, delete_limit: None) -> None:
    """
    Test Echo API
    """

    current_rate = int(get_rate)
    payload = {
        "http_throttle": "API throttle test"
    }

    # echo request through until rate limit is exhausted 
    for i in range(1, current_rate + 1):
        if i <= current_rate:
            async with AsyncClient(app=app, base_url="http://test") as async_client:
                response = await async_client.post(
                    "/echo",
                    headers={"Content-Type": "application/json"},
                    json=payload
                )
                assert response.status_code == 200
                assert response.json() == payload

        else:
            # rate limit exhausted, assert for 429
            async with AsyncClient(app=app, base_url="http://test") as async_client:
                response = await async_client.post(
                    "/echo",
                    headers={"Content-Type": "application/json"},
                    json=payload
                )
                assert response.status_code == 429
                assert response.json() == {}
