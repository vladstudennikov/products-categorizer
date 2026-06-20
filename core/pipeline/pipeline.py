from dataclasses import dataclass

from core.abstractions.executor import BaseExecutor
from core.context.pipeline_context import PipelineContext
from core.pipeline.nodes import BaseNode


@dataclass(frozen=True)
class Pipeline:
    """Executable pipeline assembled from a node graph."""

    start_node: BaseNode
    executor: BaseExecutor

    def run(
        self,
        context: PipelineContext | None = None,
    ) -> PipelineContext:
        execution_context = context if context is not None else PipelineContext()
        self.executor.execute(self.start_node, execution_context)
        return execution_context
