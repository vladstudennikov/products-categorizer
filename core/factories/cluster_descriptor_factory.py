from core.registries.cluster_descriptor_registry import (
    CLUSTER_DESCRIPTORS
)


class ClusterDescriptorFactory:
    @staticmethod
    def create(name: str, **kwargs):
        return CLUSTER_DESCRIPTORS.create(name, **kwargs)
