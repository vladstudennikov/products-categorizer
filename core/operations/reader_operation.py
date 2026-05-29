from typing import List, Optional
from core.abstractions.operation import BaseOperation
from core.abstractions.reader import BaseReader
from core.context.pipeline_context import PipelineContext


class ReaderOperation(BaseOperation):
    def __init__(
        self,
        reader: BaseReader,
    ):
        self.reader = reader

    def run(self, context: PipelineContext) -> None:
        batch = self.reader.read()
        if batch is None:
            raise ValueError("No more data to read")
        
        context.state.raw_data = batch
