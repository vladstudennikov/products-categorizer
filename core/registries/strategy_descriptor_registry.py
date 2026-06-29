from core.registries.component_registry import ComponentRegistry

STRATEGY_DESCRIPTORS = ComponentRegistry("strategy_descriptor")
STRATEGY_DESCRIPTORS.register(
    "ollama",
    "strategy_descriptor_agent.agent:StrategyAnalyzerAgent",
)
