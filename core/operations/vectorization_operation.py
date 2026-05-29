from typing import List, Optional
from core.abstractions.operation import BaseOperation
from core.abstractions.vectorizer import BaseVectorizer
from core.abstractions.validator import BaseValidator
from core.context.pipeline_context import PipelineContext


class VectorizationOperation(BaseOperation):
    def __init__(
        self,
        vectorizer: BaseVectorizer
    ):
        self.vectorizer = vectorizer

    def run(self, context: PipelineContext) -> None:
        context.state.embeddings = (
            self.vectorizer.vectorize(
                context.state.entities
            )
        )
