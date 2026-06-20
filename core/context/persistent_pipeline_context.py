import os
from core.context.pipeline_context import PipelineContext
from core.context.pipeline_state import PipelineState
from core.services.serialization_service import StatePersistenceService


class PersistentPipelineContext(PipelineContext):
    def __init__(self, persistence_dir: str = "checkpoints", **data):
        super().__init__(**data)
        self.metadata["persistence_dir"] = persistence_dir

    def checkpoint(self, name: str) -> str:
        """Saves the current state to a file."""
        return StatePersistenceService.dump_state(
            self.state, 
            self.metadata["persistence_dir"], 
            f"{name}.pkl"
        )

    def load_checkpoint(self, name: str) -> PipelineState:
        """Loads the state from a file."""
        path = os.path.join(self.metadata["persistence_dir"], f"{name}.pkl")
        self.state = StatePersistenceService.load_state(path)
        return self.state
