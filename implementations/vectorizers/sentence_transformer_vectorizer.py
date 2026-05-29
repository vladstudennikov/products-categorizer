from datetime import datetime

from sentence_transformers import SentenceTransformer

from core.abstractions.accessor import BaseAccessor
from core.abstractions.vectorizer import BaseVectorizer
from core.entities.embedding_result import EmbeddingResult


class SentenceTransformerVectorizer(BaseVectorizer):
    def __init__(self, model_name: str, accessor: BaseAccessor = None):
        super().__init__(accessor)
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def vectorize(self, entities):
        if not self.accessor:
            raise ValueError("Accessor is required for vectorization")

        texts = [
            self.accessor.get_text(entity)
            for entity in entities
        ]

        vectors = self.model.encode(texts)

        return EmbeddingResult(
            vectors=vectors,
            model_name=self.model_name,
            dimension=vectors.shape[1],
            created_at=datetime.utcnow()
        )
