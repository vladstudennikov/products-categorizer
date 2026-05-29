from abc import ABC
from abc import abstractmethod

from core.entities.cluster_result import ClusterResult
from core.entities.embedding_result import EmbeddingResult


class BaseClusterizer(ABC):
    @abstractmethod
    def cluster(
        self,
        embeddings: EmbeddingResult
    ) -> ClusterResult:
        pass
