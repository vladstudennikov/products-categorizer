from core.registries.validator_registry import (
    VALIDATORS
)
from core.factories.accessor_factory import AccessorFactory


class ValidatorFactory:

    @staticmethod
    def create(name: str, **kwargs):
        if "accessor" in kwargs and isinstance(kwargs["accessor"], str):
            kwargs["accessor"] = AccessorFactory.create(kwargs["accessor"])

        return VALIDATORS.create(name, **kwargs)
