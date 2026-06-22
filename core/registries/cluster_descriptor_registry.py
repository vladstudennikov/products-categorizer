from core.registries.component_registry import ComponentRegistry

CLUSTER_DESCRIPTORS = ComponentRegistry("cluster_descriptor")
CLUSTER_DESCRIPTORS.register(
    "ollama",
    "cluster_descriptor_agent.agent:ClusterDescriptorAgent",
)
