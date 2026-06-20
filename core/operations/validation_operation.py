from collections.abc import Iterable

from core.abstractions.operation import BaseOperation
from core.abstractions.validator import BaseValidator
from core.context.pipeline_context import PipelineContext


class ValidationOperation(BaseOperation):
    def __init__(self, validators: Iterable[BaseValidator]):
        self.validators = tuple(validators)

    def run(self, context: PipelineContext) -> None:
        for validator in self.validators:
            validator.validate(context.state)
