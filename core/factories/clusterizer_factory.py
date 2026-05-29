from core.registries.clusterizer_registry import (
    CLUSTERIZERS
)


class ClusterizerFactory:
    @staticmethod
    def create(name: str, **kwargs):
        if name not in CLUSTERIZERS:
            raise ValueError(
                f"Unknown clusterizer: {name}"
            )

        return CLUSTERIZERS[name](**kwargs)
