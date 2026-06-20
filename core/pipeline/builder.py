from collections.abc import Callable

from core.abstractions.executor import BaseExecutor
from core.abstractions.operation import BaseOperation
from core.context.pipeline_context import PipelineContext
from core.pipeline.nodes import ActionNode, BaseNode, ConditionNode


class PipelineDefinitionError(ValueError):
    """Raised when a pipeline graph is incomplete or inconsistent."""


class PipelineBuilder:
    def __init__(self):
        self.nodes: dict[str, BaseNode] = {}

    def add_node(self, node: BaseNode) -> "PipelineBuilder":
        if node.node_id in self.nodes:
            raise PipelineDefinitionError(
                f"Node id '{node.node_id}' is already present in the pipeline"
            )
        self.nodes[node.node_id] = node
        return self

    def add_operation(
        self,
        node_id: str,
        operation: BaseOperation,
    ) -> "PipelineBuilder":
        return self.add_node(ActionNode(node_id, operation))

    def add_condition(
        self,
        node_id: str,
        condition: Callable[[PipelineContext], bool],
    ) -> "PipelineBuilder":
        return self.add_node(ConditionNode(node_id, condition))

    def connect(self, source_id: str, target_id: str) -> "PipelineBuilder":
        source = self._get_node(source_id)
        target = self._get_node(target_id)
        source.connect(target)
        return self

    def chain(self, *node_ids: str) -> "PipelineBuilder":
        if len(node_ids) < 2:
            raise PipelineDefinitionError("A chain requires at least two node ids")
        for source_id, target_id in zip(node_ids, node_ids[1:]):
            self.connect(source_id, target_id)
        return self

    def branch(
        self,
        condition_id: str,
        *,
        when_true: str | None = None,
        when_false: str | None = None,
    ) -> "PipelineBuilder":
        node = self._get_node(condition_id)
        if not isinstance(node, ConditionNode):
            raise PipelineDefinitionError(
                f"Node '{condition_id}' is not a condition node"
            )
        true_node = self._get_node(when_true) if when_true is not None else None
        false_node = self._get_node(when_false) if when_false is not None else None
        node.set_branches(true_node, false_node)
        return self

    def build(self, start_node_id: str) -> BaseNode:
        return self._get_node(start_node_id)

    def build_pipeline(
        self,
        start_node_id: str,
        executor: BaseExecutor | None = None,
    ):
        from core.pipeline.executor import PipelineExecutor
        from core.pipeline.pipeline import Pipeline

        return Pipeline(
            start_node=self.build(start_node_id),
            executor=executor or PipelineExecutor(),
        )

    def _get_node(self, node_id: str) -> BaseNode:
        try:
            return self.nodes[node_id]
        except KeyError as exc:
            raise PipelineDefinitionError(
                f"Unknown pipeline node: '{node_id}'"
            ) from exc
