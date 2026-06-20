from collections import deque
from core.abstractions.executor import BaseExecutor
from core.pipeline.nodes import BaseNode
from core.context.pipeline_context import PipelineContext


class IterativeExecutor(BaseExecutor):
    """
    An executor that allows nodes to be revisited. 
    Useful for iterative processes like batching.
    Set max_steps to guard against malformed graphs with infinite loops.
    """
    def __init__(self, max_steps: int | None = None):
        if max_steps is not None and max_steps < 1:
            raise ValueError("max_steps must be greater than zero")
        self.max_steps = max_steps

    def execute(
        self,
        start_node: BaseNode,
        context: PipelineContext,
    ) -> PipelineContext:
        queue = deque([start_node])
        steps = 0

        while queue:
            if self.max_steps is not None and steps >= self.max_steps:
                raise RuntimeError(
                    f"Iterative pipeline exceeded max_steps={self.max_steps}"
                )

            node = queue.popleft()
            steps += 1
            next_nodes = node.execute(context)
            
            for next_node in next_nodes:
                if next_node:
                    queue.append(next_node)

        return context
