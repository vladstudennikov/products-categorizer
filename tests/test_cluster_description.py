import unittest
from types import SimpleNamespace
from typing import Dict, List

from core.abstractions.cluster_descriptor import BaseClusterDescriptor
from core.context.cluster_pipeline_context import ClusterPipelineContext
from core.context.cluster_pipeline_state import ClusterPipelineState
from core.operations.cluster_description_operation import ClusterDescriptionOperation
from core.pipeline.builder import PipelineBuilder
from core.factories.cluster_descriptor_factory import ClusterDescriptorFactory
from core.registries.cluster_descriptor_registry import CLUSTER_DESCRIPTORS


class FakeClusterDescriptor(BaseClusterDescriptor):
    def describe_cluster(self, product_names: List[str]) -> str:
        return f"Fake description of: {', '.join(product_names)}"

    def describe_all_clusters(self, clusters_data: Dict[str, List[str]]) -> Dict[str, str]:
        return {
            cluster_id: self.describe_cluster(names)
            for cluster_id, names in clusters_data.items()
        }


class ClusterDescriptionTests(unittest.TestCase):
    def setUp(self):
        CLUSTER_DESCRIPTORS.register("fake", FakeClusterDescriptor, replace=True)

    def test_factory_and_registry(self):
        descriptor = ClusterDescriptorFactory.create("fake")
        self.assertIsInstance(descriptor, FakeClusterDescriptor)

        res = descriptor.describe_cluster(["Product A", "Product B"])
        self.assertEqual(res, "Fake description of: Product A, Product B")

    def test_cluster_pipeline_context_defaults(self):
        context = ClusterPipelineContext()
        self.assertIsInstance(context.state, ClusterPipelineState)
        self.assertEqual(context.state.cluster_descriptions, {})

    def test_cluster_description_operation_success(self):
        descriptor = FakeClusterDescriptor()
        operation = ClusterDescriptionOperation(descriptor)

        context = ClusterPipelineContext()
        context.state.entities = [
            SimpleNamespace(name="Laptop Lenovo"),
            SimpleNamespace(name="HP Pavilion"),
            SimpleNamespace(name="MacBook Pro")
        ]
        context.state.clusters = SimpleNamespace(
            labels=[0, 1, 0],
            cluster_count=2,
            noise_count=0
        )

        operation.run(context)

        descriptions = context.state.cluster_descriptions
        self.assertIn("0", descriptions)
        self.assertIn("1", descriptions)
        self.assertEqual(descriptions["0"], "Fake description of: Laptop Lenovo, MacBook Pro")
        self.assertEqual(descriptions["1"], "Fake description of: HP Pavilion")

    def test_cluster_description_operation_failures(self):
        descriptor = FakeClusterDescriptor()
        operation = ClusterDescriptionOperation(descriptor)

        from core.context.pipeline_context import PipelineContext
        context_base = PipelineContext()
        with self.assertRaises(TypeError):
            operation.run(context_base)

        context_no_clusters = ClusterPipelineContext()
        context_no_clusters.state.entities = [SimpleNamespace(name="Prod")]
        with self.assertRaises(ValueError):
            operation.run(context_no_clusters)

        context_no_entities = ClusterPipelineContext()
        context_no_entities.state.clusters = SimpleNamespace(labels=[0])
        with self.assertRaises(ValueError):
            operation.run(context_no_entities)

        context_mismatch = ClusterPipelineContext()
        context_mismatch.state.entities = [SimpleNamespace(name="Prod")]
        context_mismatch.state.clusters = SimpleNamespace(labels=[0, 1])
        with self.assertRaises(ValueError):
            operation.run(context_mismatch)