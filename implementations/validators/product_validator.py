from core.abstractions.validator import BaseValidator
from core.abstractions.accessor import BaseAccessor


class ProductValidator(BaseValidator):
    def __init__(
        self,
        min_entities_count: int = 1,
        accessor: BaseAccessor = None
    ):
        self.min_entities_count = min_entities_count
        self.accessor = accessor

    def validate(self, data):
        if not data.entities:
            raise ValueError(
                "Entities list is empty"
            )

        if len(data.entities) < self.min_entities_count:
            raise ValueError(
                f"Insufficient entities. Need at least {self.min_entities_count}"
            )

        if not self.accessor:
            raise ValueError("Accessor is required for ProductValidator")

        for entity in data.entities:
            if not self.accessor.get_text(entity):
                raise ValueError(
                    "Entity text (extracted via accessor) cannot be empty"
                )
