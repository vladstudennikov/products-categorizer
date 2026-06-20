from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")


class BaseAccessor(ABC, Generic[T]):
    @abstractmethod
    def get_text(self, entity: T) -> str:
        """Extract text from entity for vectorization."""
        raise NotImplementedError

    @abstractmethod
    def get_id(self, entity: T) -> str:
        """Extract unique identifier from entity."""
        raise NotImplementedError
