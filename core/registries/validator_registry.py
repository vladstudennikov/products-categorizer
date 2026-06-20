from core.registries.component_registry import ComponentRegistry


VALIDATORS = ComponentRegistry("validator")
VALIDATORS.register(
    "dbscan",
    "implementations.validators.dbscan_validator:DBSCANValidator",
)
VALIDATORS.register(
    "product",
    "implementations.validators.product_validator:ProductValidator",
)
VALIDATORS.register(
    "sentence_transformer",
    "implementations.validators.sentence_transformer_validator:"
    "SentenceTransformerValidator",
)
