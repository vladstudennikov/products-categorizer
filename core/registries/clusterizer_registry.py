from core.registries.component_registry import ComponentRegistry


CLUSTERIZERS = ComponentRegistry("clusterizer")
CLUSTERIZERS.register(
    "dbscan",
    "implementations.clusterizers.dbscan_clusterizer:DBSCANClusterizer",
)
