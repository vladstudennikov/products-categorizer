from collections.abc import Callable
from abc import ABC, abstractmethod

from core.context.pipeline_context import PipelineContext
from core.abstractions.operation import BaseOperation


class BaseNode(ABC):
    def __init__(self, node_id: str):
        if not node_id or not node_id.strip():
            raise ValueError("Node id cannot be empty")
        self.node_id = node_id
        self.next_nodes: list["BaseNode"] = []

    def connect(self, node: "BaseNode") -> "BaseNode":
        if node not in self.next_nodes:
            self.next_nodes.append(node)
        return node

    @abstractmethod
    def execute(
        self,
        context: PipelineContext
    ) -> list["BaseNode"]:
        raise NotImplementedError


class ActionNode(BaseNode):
    def __init__(self, node_id: str, operation: BaseOperation):
        super().__init__(node_id)
        self.operation = operation

    def execute(self, context: PipelineContext) -> list[BaseNode]:
        self.operation.run(context)
        return self.next_nodes


class ConditionNode(BaseNode):
    def __init__(self, node_id: str, condition: Callable[[PipelineContext], bool]):
        super().__init__(node_id)
        self.condition = condition
        self.true_node: BaseNode | None = None
        self.false_node: BaseNode | None = None

    def set_branches(
        self,
        true_node: BaseNode | None,
        false_node: BaseNode | None,
    ) -> "ConditionNode":
        self.true_node = true_node
        self.false_node = false_node
        return self

    def execute(self, context: PipelineContext) -> list[BaseNode]:
        result = self.condition(context)
        branch = self.true_node if result else self.false_node
        return [branch] if branch else []
