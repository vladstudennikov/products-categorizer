from core.context.pipeline_context import PipelineContext
from core.context.cluster_pipeline_state import ClusterPipelineState
from pydantic import Field

class ClusterPipelineContext(PipelineContext):
    state: ClusterPipelineState = Field(default_factory=ClusterPipelineState)
