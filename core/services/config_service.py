import yaml


class ConfigService:
    @staticmethod
    def load(path: str) -> dict:
        with open(path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        if config is None:
            return {}
        if not isinstance(config, dict):
            raise ValueError(f"Configuration root must be a mapping: {path}")
        return config
