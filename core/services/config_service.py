import yaml


class ConfigService:
    @staticmethod
    def load(path: str):
        with open(path, "r") as file:
            return yaml.safe_load(file)
