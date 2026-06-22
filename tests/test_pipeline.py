import unittest
from types import SimpleNamespace

from core.abstractions.adapter import BaseAdapter
from core.abstractions.clusterizer import BaseClusterizer
from core.abstractions.operation import BaseOperation
from core.abstractions.reader import BaseReader
from core.abstractions.validator import BaseValidator
from core.abstractions.vectorizer import BaseVectorizer
from core.context.pipeline_context import PipelineContext
from core.operations.adapter_operation import AdapterOperation
from core.operations.clustering_operation import ClusteringOperation
from core.operations.reader_operation import ReaderOperation
from core.operations.validation_operation import ValidationOperation
from core.operations.vectorization_operation import VectorizationOperation
from core.pipeline.builder import PipelineBuilder
from core.pipeline.iterative_executor import IterativeExecutor


class StaticReader(BaseReader):
    def __init__(self, data):
        self.data = data

    def read(self):
        return self.data


class EntityAdapter(BaseAdapter):
    def transform(self, data):
        return [
            {"id": str(item["id"]), "name": item["name"].strip()}
            for item in data
        ]


class StateValidator(BaseValidator):
    def __init__(self, event_log, expected_field):
        self.event_log = event_log
        self.expected_field = expected_field

    def validate(self, state):
        self.event_log.append(f"validate:{self.expected_field}")
        if not getattr(state, self.expected_field):
            raise ValueError(f"Missing state field: {self.expected_field}")


class FakeVectorizer(BaseVectorizer):
    def __init__(self, event_log):
        super().__init__()
        self.event_log = event_log

    def vectorize(self, entities):
        self.event_log.append("vectorize")
        return SimpleNamespace(
            vectors=[[len(entity["name"])] for entity in entities],
            model_name="fake",
            dimension=1,
        )


class FakeClusterizer(BaseClusterizer):
    def __init__(self, event_log):
        self.event_log = event_log

    def cluster(self, embeddings):
        self.event_log.append("cluster")
        labels = [index % 2 for index, _ in enumerate(embeddings.vectors)]
        return SimpleNamespace(
            labels=labels,
            cluster_count=len(set(labels)),
            noise_count=0,
        )


class RecordOperation(BaseOperation):
    def __init__(self, value):
        self.value = value

    def run(self, context):
        context.metadata.setdefault("events", []).append(self.value)


class FailingOperation(BaseOperation):
    def run(self, context):
        context.metadata.setdefault("events", []).append("failed")
        raise RuntimeError("operation failed")


class IncrementOperation(BaseOperation):
    def run(self, context):
        context.metadata["count"] = context.metadata.get("count", 0) + 1


class PipelineExecutionTests(unittest.TestCase):
    def test_complete_product_processing_pipeline(self):
        event_log = []
        reader = StaticReader(
            [
                {"id": 1, "name": " Phone "},
                {"id": 2, "name": "Case"},
                {"id": 3, "name": "Cable"},
            ]
        )

        pipeline = (
            PipelineBuilder()
            .add_operation("read", ReaderOperation(reader))
            .add_operation("adapt", AdapterOperation(EntityAdapter()))
            .add_operation(
                "validate_entities",
                ValidationOperation([StateValidator(event_log, "entities")]),
            )
            .add_operation(
                "vectorize",
                VectorizationOperation(FakeVectorizer(event_log)),
            )
            .add_operation(
                "validate_embeddings",
                ValidationOperation([StateValidator(event_log, "embeddings")]),
            )
            .add_operation(
                "cluster",
                ClusteringOperation(FakeClusterizer(event_log)),
            )
            .chain(
                "read",
                "adapt",
                "validate_entities",
                "vectorize",
                "validate_embeddings",
                "cluster",
            )
            .build_pipeline("read")
        )

        context = pipeline.run()

        self.assertEqual(
            event_log,
            [
                "validate:entities",
                "vectorize",
                "validate:embeddings",
                "cluster",
            ],
        )
        self.assertEqual(context.state.entities[0]["name"], "Phone")
        self.assertEqual(context.state.embeddings.vectors, [[5], [4], [5]])
        self.assertEqual(context.state.clusters.labels, [0, 1, 0])
        self.assertEqual(context.state.clusters.cluster_count, 2)

    def test_pipeline_uses_and_returns_supplied_context(self):
        supplied_context = PipelineContext(metadata={"request_id": "request-1"})
        pipeline = (
            PipelineBuilder()
            .add_operation("record", RecordOperation("executed"))
            .build_pipeline("record")
        )

        returned_context = pipeline.run(supplied_context)

        self.assertIs(returned_context, supplied_context)
        self.assertEqual(returned_context.metadata["request_id"], "request-1")
        self.assertEqual(returned_context.metadata["events"], ["executed"])

    def test_sequential_nodes_execute_in_declared_order(self):
        pipeline = (
            PipelineBuilder()
            .add_operation("first", RecordOperation("first"))
            .add_operation("second", RecordOperation("second"))
            .add_operation("third", RecordOperation("third"))
            .chain("first", "second", "third")
            .build_pipeline("first")
        )

        context = pipeline.run()

        self.assertEqual(context.metadata["events"], ["first", "second", "third"])

    def test_true_and_false_branches_execute_only_selected_path(self):
        builder = (
            PipelineBuilder()
            .add_condition(
                "condition",
                lambda context: context.metadata["select_true"],
            )
            .add_operation("true", RecordOperation("true"))
            .add_operation("false", RecordOperation("false"))
            .branch("condition", when_true="true", when_false="false")
        )
        pipeline = builder.build_pipeline("condition")

        true_context = pipeline.run(
            PipelineContext(metadata={"select_true": True})
        )
        false_context = pipeline.run(
            PipelineContext(metadata={"select_true": False})
        )

        self.assertEqual(true_context.metadata["events"], ["true"])
        self.assertEqual(false_context.metadata["events"], ["false"])

    def test_shared_downstream_node_executes_once_with_standard_executor(self):
        builder = (
            PipelineBuilder()
            .add_operation("start", RecordOperation("start"))
            .add_operation("left", RecordOperation("left"))
            .add_operation("right", RecordOperation("right"))
            .add_operation("join", RecordOperation("join"))
        )
        builder.connect("start", "left")
        builder.connect("start", "right")
        builder.connect("left", "join")
        builder.connect("right", "join")

        context = builder.build_pipeline("start").run()

        self.assertEqual(
            context.metadata["events"],
            ["start", "left", "right", "join"],
        )

    def test_operation_failure_stops_downstream_execution(self):
        pipeline = (
            PipelineBuilder()
            .add_operation("before", RecordOperation("before"))
            .add_operation("failure", FailingOperation())
            .add_operation("after", RecordOperation("after"))
            .chain("before", "failure", "after")
            .build_pipeline("before")
        )
        context = PipelineContext()

        with self.assertRaisesRegex(RuntimeError, "operation failed"):
            pipeline.run(context)

        self.assertEqual(context.metadata["events"], ["before", "failed"])

    def test_iterative_executor_revisits_nodes_until_condition_finishes(self):
        builder = (
            PipelineBuilder()
            .add_operation("increment", IncrementOperation())
            .add_condition(
                "continue",
                lambda context: context.metadata["count"] < 3,
            )
            .add_operation("done", RecordOperation("done"))
            .connect("increment", "continue")
            .branch("continue", when_true="increment", when_false="done")
        )
        pipeline = builder.build_pipeline(
            "increment",
            executor=IterativeExecutor(max_steps=10),
        )

        context = pipeline.run()

        self.assertEqual(context.metadata["count"], 3)
        self.assertEqual(context.metadata["events"], ["done"])


class PipelineOperationContractTests(unittest.TestCase):
    def test_reader_rejects_exhausted_source(self):
        operation = ReaderOperation(StaticReader(None))

        with self.assertRaisesRegex(ValueError, "No more data"):
            operation.run(PipelineContext())

    def test_adapter_requires_raw_data(self):
        operation = AdapterOperation(EntityAdapter())

        with self.assertRaisesRegex(ValueError, "No raw data"):
            operation.run(PipelineContext())

    def test_vectorization_requires_entities(self):
        operation = VectorizationOperation(FakeVectorizer([]))

        with self.assertRaisesRegex(ValueError, "No entities"):
            operation.run(PipelineContext())

    def test_clustering_requires_embeddings(self):
        operation = ClusteringOperation(FakeClusterizer([]))

        with self.assertRaisesRegex(ValueError, "No embeddings"):
            operation.run(PipelineContext())

    def test_validation_runs_all_validators_in_order(self):
        event_log = []
        context = PipelineContext()
        context.state.entities = [{"id": "1", "name": "Phone"}]
        operation = ValidationOperation(
            [
                StateValidator(event_log, "entities"),
                StateValidator(event_log, "entities"),
            ]
        )

        operation.run(context)

        self.assertEqual(
            event_log,
            ["validate:entities", "validate:entities"],
        )


if __name__ == "__main__":
    unittest.main()