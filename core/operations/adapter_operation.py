from collections.abc import Iterable
from typing import Any

from core.abstractions.adapter import BaseAdapter
from core.abstractions.operation import BaseOperation
from core.context.pipeline_context import PipelineContext


class AdapterOperation(BaseOperation):
    """Adapt raw reader output into the entities used by the pipeline."""

    def __init__(self, adapter: BaseAdapter[Any, Iterable[Any]]):
        self.adapter = adapter

    def run(self, context: PipelineContext) -> None:
        if context.state.raw_data is None:
            raise ValueError("No raw data found in context state")

        entities = self.adapter.transform(context.state.raw_data)
        if entities is None:
            raise ValueError("Adapter returned no entities")

        context.state.entities = list(entities)
