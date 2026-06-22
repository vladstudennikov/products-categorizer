from core.context.pipeline_state import PipelineState
from pydantic import Field

class ClusterPipelineState(PipelineState):
    cluster_descriptions: dict[str, str] = Field(default_factory=dict)
