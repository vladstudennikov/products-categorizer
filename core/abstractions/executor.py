from abc import ABC, abstractmethod
from core.pipeline.nodes import BaseNode
from core.context.pipeline_context import PipelineContext


class BaseExecutor(ABC):
    @abstractmethod
    def execute(
        self,
        start_node: BaseNode,
        context: PipelineContext,
    ) -> PipelineContext:
        """Executes the pipeline starting from the given node."""
        raise NotImplementedError
