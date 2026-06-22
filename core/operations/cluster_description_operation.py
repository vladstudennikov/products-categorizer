from core.abstractions.operation import BaseOperation
from core.abstractions.cluster_descriptor import BaseClusterDescriptor
from core.context.pipeline_context import PipelineContext

class ClusterDescriptionOperation(BaseOperation):
    def __init__(self, descriptor: BaseClusterDescriptor):
        self.descriptor = descriptor

    def run(self, context: PipelineContext) -> None:
        if not hasattr(context.state, 'cluster_descriptions'):
            raise TypeError(
                "Context state does not support cluster_descriptions. "
                "Please use ClusterPipelineState or a state with the 'cluster_descriptions' field."
            )

        if context.state.clusters is None:
            raise ValueError("No clusters found in context state")

        if not context.state.entities:
            raise ValueError("No entities found in context state")

        if len(context.state.clusters.labels) != len(context.state.entities):
            raise ValueError(
                f"Mismatched size: labels size ({len(context.state.clusters.labels)}) and entities size ({len(context.state.entities)}) must be equal."
            )

        clusters_data = {}
        for entity, label in zip(context.state.entities, context.state.clusters.labels):
            if str(label) not in clusters_data:
                clusters_data[str(label)] = []
            
            clusters_data[str(label)].append(getattr(entity, 'name', str(entity)))

        context.state.cluster_descriptions = self.descriptor.describe_all_clusters(clusters_data)
