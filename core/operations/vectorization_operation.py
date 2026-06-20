from core.abstractions.operation import BaseOperation
from core.abstractions.vectorizer import BaseVectorizer
from core.context.pipeline_context import PipelineContext


class VectorizationOperation(BaseOperation):
    def __init__(
        self,
        vectorizer: BaseVectorizer
    ):
        self.vectorizer = vectorizer

    def run(self, context: PipelineContext) -> None:
        if not context.state.entities:
            raise ValueError("No entities found in context state")

        context.state.embeddings = (
            self.vectorizer.vectorize(
                context.state.entities
            )
        )
