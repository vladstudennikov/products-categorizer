from core.registries.vectorizer_registry import (
    VECTORIZERS
)
from core.factories.accessor_factory import AccessorFactory


class VectorizerFactory:
    @staticmethod
    def create(name: str, **kwargs):
        if "accessor" in kwargs and isinstance(kwargs["accessor"], str):
            kwargs["accessor"] = AccessorFactory.create(kwargs["accessor"])

        return VECTORIZERS.create(name, **kwargs)
