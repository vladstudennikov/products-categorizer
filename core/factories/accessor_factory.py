from core.registries.accessor_registry import (
    ACCESSORS
)


class AccessorFactory:
    @staticmethod
    def create(name: str, **kwargs):
        return ACCESSORS.create(name, **kwargs)
