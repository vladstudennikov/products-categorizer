from abc import ABC
from abc import abstractmethod


class BaseAdapter(ABC):
    @abstractmethod
    def transform(self, data):
        pass
