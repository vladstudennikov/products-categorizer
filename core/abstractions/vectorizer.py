from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from core.entities.embedding_result import EmbeddingResult
from core.abstractions.accessor import BaseAccessor

T = TypeVar("T")


class BaseVectorizer(ABC, Generic[T]):
    def __init__(self, accessor: BaseAccessor[T] | None = None):
        self.accessor = accessor

    @abstractmethod
    def vectorize(
        self,
        entities: list[T]
    ) -> EmbeddingResult:
        raise NotImplementedError
