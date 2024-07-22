from abc import ABC, abstractmethod
from typing import Any


class BaseStorage(ABC):

    @abstractmethod
    async def transform(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    async def add(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    async def search(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    async def search_many(self, *args, **kwargs) -> Any:
        pass