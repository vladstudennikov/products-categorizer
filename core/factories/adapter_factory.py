from core.registries.adapter_registry import ADAPTERS


class AdapterFactory:
    @staticmethod
    def create(name: str, **kwargs):
        return ADAPTERS.create(name, **kwargs)
