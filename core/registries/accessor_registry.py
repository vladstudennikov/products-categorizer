from core.registries.component_registry import ComponentRegistry


ACCESSORS = ComponentRegistry("accessor")
ACCESSORS.register(
    "product",
    "implementations.accessors.product_accessor:ProductAccessor",
)
