from pydantic import BaseModel


class ClusterResult(BaseModel):
    labels: list[int]
    cluster_count: int
    noise_count: int
