from collections import deque
from core.abstractions.executor import BaseExecutor
from core.pipeline.nodes import BaseNode
from core.context.pipeline_context import PipelineContext


class IterativeExecutor(BaseExecutor):
    """
    An executor that allows nodes to be revisited. 
    Useful for iterative processes like batching.
    Warning: Malformed graphs with infinite loops will cause a hang.
    """
    def execute(self, start_node: BaseNode, context: PipelineContext) -> None:
        queue = deque([start_node])

        while queue:
            node = queue.popleft()
            next_nodes = node.execute(context)
            
            for next_node in next_nodes:
                if next_node:
                    queue.append(next_node)
