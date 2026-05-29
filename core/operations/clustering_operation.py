from typing import List, Optional
from core.abstractions.operation import BaseOperation
from core.abstractions.clusterizer import BaseClusterizer
from core.abstractions.validator import BaseValidator
from core.context.pipeline_context import PipelineContext


class ClusteringOperation(BaseOperation):
    def __init__(
        self,
        clusterizer: BaseClusterizer
    ):
        self.clusterizer = clusterizer

    def run(self, context: PipelineContext) -> None:
        if context.state.embeddings is None:
            raise ValueError("No embeddings found in context state")

        context.state.clusters = (
            self.clusterizer.cluster(
                context.state.embeddings
            )
        )
