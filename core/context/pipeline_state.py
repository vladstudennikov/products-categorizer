from typing import Any

from pydantic import BaseModel, Field

from core.entities.cluster_result import ClusterResult
from core.entities.embedding_result import EmbeddingResult


class PipelineState(BaseModel):
    raw_data: Any | None = None
    entities: list[Any] = Field(default_factory=list)
    embeddings: EmbeddingResult | None = None
    clusters: ClusterResult | None = None
