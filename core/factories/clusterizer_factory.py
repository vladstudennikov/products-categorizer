from core.registries.clusterizer_registry import (
    CLUSTERIZERS
)


class ClusterizerFactory:
    @staticmethod
    def create(name: str, **kwargs):
        return CLUSTERIZERS.create(name, **kwargs)
