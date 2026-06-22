from abc import ABC, abstractmethod
from typing import List, Dict

class BaseClusterDescriptor(ABC):
    @abstractmethod
    def describe_cluster(self, product_names: List[str]) -> str:
        """Describe a single cluster given its product names."""
        raise NotImplementedError

    @abstractmethod
    def describe_all_clusters(self, clusters_data: Dict[str, List[str]]) -> Dict[str, str]:
        """Describe all clusters given a dictionary mapping cluster_ids to lists of product names."""
        raise NotImplementedError
