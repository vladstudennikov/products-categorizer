from core.context.cluster_pipeline_state import ClusterPipelineState
from pydantic import Field

class StrategyPipelineState(ClusterPipelineState):
    strategy_report: str | None = None