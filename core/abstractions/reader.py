from abc import ABC, abstractmethod
from typing import Any


class BaseReader(ABC):
    @abstractmethod
    def read(self) -> Any | None:
        """Return the next batch, or None when the source is exhausted."""
        raise NotImplementedError
