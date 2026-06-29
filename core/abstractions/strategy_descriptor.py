from abc import ABC, abstractmethod

class BaseStrategyDescriptor(ABC):
    @abstractmethod
    def analyze_strategy(self) -> str:
        raise NotImplementedError
