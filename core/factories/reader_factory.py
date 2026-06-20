from core.registries.reader_registry import READERS


class ReaderFactory:
    @staticmethod
    def create(name: str, **kwargs):
        return READERS.create(name, **kwargs)
