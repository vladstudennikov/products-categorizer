from core.abstractions.validator import BaseValidator


class DBSCANValidator(BaseValidator):
    def __init__(
        self,
        max_eps_allowed: float,
        min_samples_required: int
    ):
        self.max_eps_allowed = max_eps_allowed
        self.min_samples_required = min_samples_required

    def validate(self, data):
        if data.embeddings is None:
            raise ValueError(
                "Clustering Error: No embeddings found in pipeline state"
            )

        # Here we use the RULES from validators.yaml to check the actual STATE
        # Note: In a real app, you might check if the 'embeddings' object 
        # itself has metadata that violates these rules.
