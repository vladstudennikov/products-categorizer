import unittest

from core.abstractions.adapter import BaseAdapter
from core.abstractions.operation import BaseOperation
from core.abstractions.reader import BaseReader
from core.context.pipeline_context import PipelineContext
from core.operations.adapter_operation import AdapterOperation
from core.operations.reader_operation import ReaderOperation
from core.pipeline.builder import PipelineBuilder, PipelineDefinitionError
from core.pipeline.iterative_executor import IterativeExecutor
from core.registries.component_registry import ComponentRegistry


class ListReader(BaseReader):
    def __init__(self, values):
        self.values = values

    def read(self):
        return self.values


class DictAdapter(BaseAdapter):
    def transform(self, data):
        return [{"id": value, "name": str(value)} for value in data]


class RecordOperation(BaseOperation):
    def __init__(self, value):
        self.value = value

    def run(self, context):
        context.metadata.setdefault("visited", []).append(self.value)


class CoreArchitectureTests(unittest.TestCase):
    def test_context_defaults_are_not_shared(self):
        first = PipelineContext()
        second = PipelineContext()

        first.state.entities.append("entity")
        first.metadata["key"] = "value"

        self.assertEqual(second.state.entities, [])
        self.assertEqual(second.metadata, {})

    def test_reader_adapter_pipeline(self):
        pipeline = (
            PipelineBuilder()
            .add_operation("read", ReaderOperation(ListReader([1, 2])))
            .add_operation("adapt", AdapterOperation(DictAdapter()))
            .chain("read", "adapt")
            .build_pipeline("read")
        )

        context = pipeline.run()

        self.assertEqual(
            context.state.entities,
            [{"id": 1, "name": "1"}, {"id": 2, "name": "2"}],
        )

    def test_builder_rejects_duplicate_and_unknown_nodes(self):
        builder = PipelineBuilder().add_operation("one", RecordOperation(1))

        with self.assertRaises(PipelineDefinitionError):
            builder.add_operation("one", RecordOperation(2))

        with self.assertRaises(PipelineDefinitionError):
            builder.connect("one", "missing")

    def test_condition_branches(self):
        pipeline = (
            PipelineBuilder()
            .add_condition("condition", lambda context: context.metadata["use_true"])
            .add_operation("true", RecordOperation("true"))
            .add_operation("false", RecordOperation("false"))
            .branch("condition", when_true="true", when_false="false")
            .build_pipeline("condition")
        )

        context = pipeline.run(PipelineContext(metadata={"use_true": False}))

        self.assertEqual(context.metadata["visited"], ["false"])

    def test_registry_supports_runtime_registration(self):
        registry = ComponentRegistry("example")

        @registry.register("component")
        class Component:
            def __init__(self, value):
                self.value = value

        self.assertEqual(registry.create("component", value=3).value, 3)

        with self.assertRaisesRegex(ValueError, "Available: component"):
            registry.create("missing")

    def test_iterative_executor_has_optional_safety_limit(self):
        builder = PipelineBuilder().add_operation("loop", RecordOperation("loop"))
        builder.connect("loop", "loop")
        pipeline = builder.build_pipeline(
            "loop",
            executor=IterativeExecutor(max_steps=2),
        )

        with self.assertRaisesRegex(RuntimeError, "max_steps=2"):
            pipeline.run()


if __name__ == "__main__":
    unittest.main()
