from core.registries.accessor_registry import (
    ACCESSORS
)


class AccessorFactory:
    @staticmethod
    def create(name: str, **kwargs):
        if name not in ACCESSORS:
            raise ValueError(
                f"Unknown accessor: {name}"
            )

        return ACCESSORS[name](**kwargs)
