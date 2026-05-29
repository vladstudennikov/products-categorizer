from abc import ABC
from abc import abstractmethod


class BaseValidator(ABC):
    @abstractmethod
    def validate(self, data):
        pass
