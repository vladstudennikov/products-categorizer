from core.registries.strategy_descriptor_registry import (
    STRATEGY_DESCRIPTORS
)


class StrategyDescriptorFactory:
    @staticmethod
    def create(name: str, **kwargs):
        return STRATEGY_DESCRIPTORS.create(name, **kwargs)
