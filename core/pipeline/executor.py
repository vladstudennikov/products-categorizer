from collections import deque
from core.abstractions.executor import BaseExecutor
from core.pipeline.nodes import BaseNode
from core.context.pipeline_context import PipelineContext


class PipelineExecutor(BaseExecutor):
    def execute(self, start_node: BaseNode, context: PipelineContext) -> None:
        queue = deque([start_node])
        visited = set()

        while queue:
            node = queue.popleft()

            if node.node_id in visited:
                continue

            visited.add(node.node_id)
            next_nodes = node.execute(context)
            
            for next_node in next_nodes:
                if next_node:
                    queue.append(next_node)
