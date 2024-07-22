from abc import ABC, abstractmethod
from typing import Any


class BaseCache(ABC):
    @abstractmethod
    async def get_from_cache(self, url: str):
        pass

    @abstractmethod
    async def put_to_cache(self, url: str, data: Any):
        pass
