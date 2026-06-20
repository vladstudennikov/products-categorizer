import pickle
import os
from typing import Any
from core.context.pipeline_state import PipelineState


class StatePersistenceService:
    @staticmethod
    def dump_state(state: PipelineState, directory: str, filename: str = "state.pkl") -> str:
        """Dumps the entire pipeline state to a file."""
        os.makedirs(directory, exist_ok=True)
        
        path = os.path.join(directory, filename)
        with open(path, "wb") as f:
            pickle.dump(state, f)
        return path

    @staticmethod
    def load_state(path: str) -> PipelineState:
        """Loads a pipeline state from a file."""
        with open(path, "rb") as f:
            return pickle.load(f)

    @staticmethod
    def dump_component(component: Any, directory: str, name: str) -> str:
        """Dumps a specific component (e.g., embeddings) to a file."""
        os.makedirs(directory, exist_ok=True)
            
        path = os.path.join(directory, f"{name}.pkl")
        with open(path, "wb") as f:
            pickle.dump(component, f)
        return path

    @staticmethod
    def load_component(path: str) -> Any:
        """Loads a component from a file."""
        with open(path, "rb") as f:
            return pickle.load(f)
