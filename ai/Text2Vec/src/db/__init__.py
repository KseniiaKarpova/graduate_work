from abc import ABC, abstractmethod
from typing import Any, List

from shemas import ResponseDB


class BaseVecDB(ABC):

    @abstractmethod
    async def add(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    async def search(self, *args, **kwargs) -> ResponseDB:
        pass

    @abstractmethod
    async def search_many(self, *args, **kwargs) -> List[ResponseDB]:
        pass
