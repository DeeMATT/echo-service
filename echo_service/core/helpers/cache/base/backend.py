from abc import ABC, abstractmethod
from typing import Any


class BaseBackend(ABC):
    @abstractmethod
    async def get(self, key: str) -> Any:
        ...

    @abstractmethod
    async def set(self, key: str, value: str, ttl: int = 60) -> None:
        ...

    @abstractmethod
    async def incr(self, key: str) -> None:
        ...

    @abstractmethod
    async def delete(self, key: str) -> None:
        ...
