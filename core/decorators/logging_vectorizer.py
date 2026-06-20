from typing import Any
from core.abstractions.vectorizer import BaseVectorizer
from core.entities.embedding_result import EmbeddingResult


class LoggingVectorizer(BaseVectorizer):
    def __init__(self, wrapped: BaseVectorizer, logger: Any):
        super().__init__(accessor=getattr(wrapped, 'accessor', None))
        self.wrapped = wrapped
        self.logger = logger

    def vectorize(self, entities: list[Any]) -> EmbeddingResult:
        self.logger.info(f"Vectorizing {len(entities)} entities")
        result = self.wrapped.vectorize(entities)
        self.logger.info("Vectorization completed")
        return result
