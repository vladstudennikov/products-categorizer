from abc import ABC
from abc import abstractmethod


from typing import Any, Optional


class BaseReader(ABC):
    @abstractmethod
    def read(self) -> Optional[Any]:
        pass
