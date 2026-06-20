from core.registries.component_registry import ComponentRegistry


ADAPTERS = ComponentRegistry("adapter")
ADAPTERS.register(
    "excel_product",
    "implementations.adapters.excel_product_adapter:ExcelProductAdapter",
)
