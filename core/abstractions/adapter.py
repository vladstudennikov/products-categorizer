from abc import ABC, abstractmethod
from typing import Generic, TypeVar

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


class BaseAdapter(ABC, Generic[InputT, OutputT]):
    @abstractmethod
    def transform(self, data: InputT) -> OutputT:
        """Convert reader output into entities understood by later stages."""
        raise NotImplementedError
