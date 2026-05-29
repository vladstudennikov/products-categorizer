from core.abstractions.operation import BaseOperation
from core.context.pipeline_context import PipelineContext


class PersistenceNotSupportedError(Exception):
    """Raised when a persistence operation is attempted on a context that doesn't support it."""
    pass


class StatePersistenceOperation(BaseOperation):
    def __init__(self, checkpoint_name: str):
        self.checkpoint_name = checkpoint_name

    def run(self, context: PipelineContext) -> None:
        if not hasattr(context, "checkpoint"):
            raise PersistenceNotSupportedError(
                f"Context of type {type(context).__name__} does not support checkpointing."
            )
        
        context.checkpoint(self.checkpoint_name)
