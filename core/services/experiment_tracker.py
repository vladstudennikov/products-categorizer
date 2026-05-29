import json


class ExperimentTracker:
    def save_metadata(self, path, metadata):
        with open(path, "w") as file:
            json.dump(
                metadata.model_dump(),
                file,
                indent=4,
                default=str
            )
