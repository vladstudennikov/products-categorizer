from typing import Dict
from core.pipeline.nodes import BaseNode


class PipelineBuilder:
    def __init__(self):
        self.nodes: Dict[str, BaseNode] = {}

    def add_node(self, node: BaseNode) -> "PipelineBuilder":
        self.nodes[node.node_id] = node
        return self

    def connect(self, source_id: str, target_id: str) -> "PipelineBuilder":
        self.nodes[source_id].connect(
            self.nodes[target_id]
        )
        return self

    def build(self, start_node_id: str) -> BaseNode:
        return self.nodes[start_node_id]
