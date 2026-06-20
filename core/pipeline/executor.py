from collections import deque
from core.abstractions.executor import BaseExecutor
from core.pipeline.nodes import BaseNode
from core.context.pipeline_context import PipelineContext


class PipelineExecutor(BaseExecutor):
    def execute(
        self,
        start_node: BaseNode,
        context: PipelineContext,
    ) -> PipelineContext:
        queue = deque([start_node])
        visited: set[int] = set()

        while queue:
            node = queue.popleft()
            node_identity = id(node)

            if node_identity in visited:
                continue

            visited.add(node_identity)
            next_nodes = node.execute(context)
            
            for next_node in next_nodes:
                if next_node:
                    queue.append(next_node)

        return context
