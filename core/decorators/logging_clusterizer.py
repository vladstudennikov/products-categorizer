from typing import Any
from core.abstractions.clusterizer import BaseClusterizer
from core.entities.embedding_result import EmbeddingResult
from core.entities.cluster_result import ClusterResult


class LoggingClusterizer(BaseClusterizer):
    def __init__(self, wrapped: BaseClusterizer, logger: Any):
        self.wrapped = wrapped
        self.logger = logger

    def cluster(self, embeddings: EmbeddingResult) -> ClusterResult:
        self.logger.info("Clustering started")
        result = self.wrapped.cluster(embeddings)
        self.logger.info(f"Clusters found: {result.cluster_count}")
        return result
