from abc import ABC
from abc import abstractmethod

from core.context.pipeline_context import PipelineContext


class BaseOperation(ABC):
    @abstractmethod
    def run(self, context: PipelineContext) -> None:
        """Read from and/or update the pipeline context."""
        raise NotImplementedError
