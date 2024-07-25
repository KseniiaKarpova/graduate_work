from abc import ABC

from beanie import Document


class BaseStorage(ABC):
    document: Document | None = None
