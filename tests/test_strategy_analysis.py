import unittest
from types import SimpleNamespace
from typing import Dict, List

from core.abstractions.strategy_descriptor import BaseStrategyDescriptor
from core.context.strategy_pipeline_context import StrategyPipelineContext
from core.context.strategy_pipeline_state import StrategyPipelineState
from core.operations.strategy_analysis_operation import StrategyAnalysisOperation
from core.pipeline.builder import PipelineBuilder
from core.factories.strategy_descriptor_factory import StrategyDescriptorFactory
from core.registries.strategy_descriptor_registry import STRATEGY_DESCRIPTORS


class FakeStrategyDescriptor(BaseStrategyDescriptor):
    def analyze_strategy(self, competitor_products_path: str = "data/products_other_company.csv") -> str:
        return f"Fake strategy analysis using {competitor_products_path}"


class StrategyAnalysisTests(unittest.TestCase):
    def setUp(self):
        STRATEGY_DESCRIPTORS.register("fake", FakeStrategyDescriptor, replace=True)

    def test_factory_and_registry(self):
        descriptor = StrategyDescriptorFactory.create("fake")
        self.assertIsInstance(descriptor, FakeStrategyDescriptor)

        res = descriptor.analyze_strategy("data/test_comp.csv")
        self.assertEqual(res, "Fake strategy analysis using data/test_comp.csv")

    def test_factory_ollama_creation(self):
        descriptor = StrategyDescriptorFactory.create("ollama")
        self.assertEqual(descriptor.__class__.__name__, "StrategyAnalyzerAgent")

    def test_strategy_pipeline_context_defaults(self):
        context = StrategyPipelineContext()
        self.assertIsInstance(context.state, StrategyPipelineState)
        self.assertEqual(context.state.strategy_report, None)
        self.assertEqual(context.state.competitor_products_path, "data/products_other_company.csv")

    def test_strategy_analysis_operation_success(self):
        descriptor = FakeStrategyDescriptor()
        operation = StrategyAnalysisOperation(descriptor)

        context = StrategyPipelineContext()
        context.state.competitor_products_path = "data/custom_competitor.csv"

        operation.run(context)

        self.assertEqual(context.state.strategy_report, "Fake strategy analysis using data/custom_competitor.csv")

    def test_strategy_analysis_operation_failures(self):
        descriptor = FakeStrategyDescriptor()
        operation = StrategyAnalysisOperation(descriptor)

        from core.context.pipeline_context import PipelineContext
        context_base = PipelineContext()
        with self.assertRaises(TypeError):
            operation.run(context_base)


if __name__ == "__main__":
    unittest.main()
