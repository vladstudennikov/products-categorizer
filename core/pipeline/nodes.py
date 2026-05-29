from typing import List, Callable
from abc import ABC
from abc import abstractmethod

from core.context.pipeline_context import PipelineContext
from core.abstractions.operation import BaseOperation


class BaseNode(ABC):
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.next_nodes: List["BaseNode"] = []

    def connect(self, node: "BaseNode"):
        self.next_nodes.append(node)

    @abstractmethod
    def execute(
        self,
        context: PipelineContext
    ) -> List["BaseNode"]:
        pass


class ActionNode(BaseNode):
    def __init__(self, node_id: str, operation: BaseOperation):
        super().__init__(node_id)
        self.operation = operation

    def execute(self, context: PipelineContext) -> List[BaseNode]:
        self.operation.run(context)
        return self.next_nodes


class ConditionNode(BaseNode):
    def __init__(self, node_id: str, condition: Callable[[PipelineContext], bool]):
        super().__init__(node_id)
        self.condition = condition
        self.true_node: BaseNode | None = None
        self.false_node: BaseNode | None = None

    def set_branches(self, true_node: BaseNode, false_node: BaseNode):
        self.true_node = true_node
        self.false_node = false_node

    def execute(self, context: PipelineContext) -> List[BaseNode]:
        result = self.condition(context)
        branch = self.true_node if result else self.false_node
        return [branch] if branch else []
