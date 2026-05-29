from core.abstractions.validator import BaseValidator


class SentenceTransformerValidator(BaseValidator):
    def __init__(self, expected_model_name: str):
        self.expected_model_name = expected_model_name

    def validate(self, data):
        if not self.expected_model_name:
            raise ValueError(
                "Validator configuration error: expected_model_name is empty"
            )

        if not data.entities:
            raise ValueError(
                "Cannot vectorize: Entities are missing in pipeline state"
            )
