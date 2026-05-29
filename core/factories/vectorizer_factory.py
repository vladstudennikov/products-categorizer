from core.registries.vectorizer_registry import (
    VECTORIZERS
)
from core.factories.accessor_factory import AccessorFactory


class VectorizerFactory:
    @staticmethod
    def create(name: str, **kwargs):
        if name not in VECTORIZERS:
            raise ValueError(
                f"Unknown vectorizer: {name}"
            )

        if "accessor" in kwargs and isinstance(kwargs["accessor"], str):
            kwargs["accessor"] = AccessorFactory.create(kwargs["accessor"])

        return VECTORIZERS[name](**kwargs)
