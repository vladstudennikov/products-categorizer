from typing import Any

from pydantic import BaseModel, Field

from core.context.pipeline_state import PipelineState


class PipelineContext(BaseModel):
    state: PipelineState = Field(default_factory=PipelineState)
    metadata: dict[str, Any] = Field(default_factory=dict)
