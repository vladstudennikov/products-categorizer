from pydantic import BaseModel

from core.context.pipeline_state import PipelineState


class PipelineContext(BaseModel):
    state: PipelineState = PipelineState()
    metadata: dict = {}
