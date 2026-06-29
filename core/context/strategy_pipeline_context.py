from core.context.pipeline_context import PipelineContext
from core.context.strategy_pipeline_state import StrategyPipelineState
from pydantic import Field

class StrategyPipelineContext(PipelineContext):
    state: StrategyPipelineState = Field(default_factory=StrategyPipelineState)
