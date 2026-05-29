from sklearn.cluster import DBSCAN

from core.abstractions.clusterizer import BaseClusterizer
from core.entities.cluster_result import ClusterResult


class DBSCANClusterizer(BaseClusterizer):
    def __init__(
        self,
        eps: float,
        min_samples: int
    ):
        self.eps = eps
        self.min_samples = min_samples

        self.model = DBSCAN(
            eps=eps,
            min_samples=min_samples
        )

    def cluster(self, embeddings):
        labels = self.model.fit_predict(
            embeddings.vectors
        )

        unique_clusters = {
            label
            for label in labels
            if label != -1
        }

        noise_count = list(labels).count(-1)

        return ClusterResult(
            labels=list(labels),
            cluster_count=len(unique_clusters),
            noise_count=noise_count
        )
