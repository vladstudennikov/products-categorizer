from datetime import datetime

from pydantic import BaseModel


class ExperimentMetadata(BaseModel):
    experiment_name: str
    timestamp: datetime
    vectorizer_name: str
    clusterizer_name: str
    dataset_hash: str
    parameters: dict
