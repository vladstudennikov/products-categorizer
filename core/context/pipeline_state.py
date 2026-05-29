from typing import Any

from pydantic import BaseModel

from core.entities.cluster_result import ClusterResult
from core.entities.embedding_result import EmbeddingResult
from core.entities.product import Product


class PipelineState(BaseModel):
    raw_data: list[Any] | None = None
    entities: list[Product] = []
    embeddings: EmbeddingResult | None = None
    clusters: ClusterResult | None = None
