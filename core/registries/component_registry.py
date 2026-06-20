from collections.abc import Callable, Iterator, Mapping
from importlib import import_module
from typing import Any


ComponentFactory = Callable[..., Any]
ComponentDefinition = ComponentFactory | type | str


class ComponentRegistry(Mapping[str, ComponentFactory]):
    """Named component definitions with optional lazy imports.

    Third-party code can register components at application startup without
    editing the core package. Import paths keep optional dependencies unloaded
    until the corresponding component is actually created.
    """

    def __init__(self, component_kind: str):
        self.component_kind = component_kind
        self._definitions: dict[str, ComponentDefinition] = {}

    def register(
        self,
        name: str,
        component: ComponentDefinition | None = None,
        *,
        replace: bool = False,
    ):
        if not name or not name.strip():
            raise ValueError("Component name cannot be empty")

        def add(definition: ComponentDefinition):
            if name in self._definitions and not replace:
                raise ValueError(
                    f"{self.component_kind.capitalize()} '{name}' is already registered"
                )
            self._definitions[name] = definition
            return definition

        return add(component) if component is not None else add

    def create(self, name: str, **kwargs: Any) -> Any:
        try:
            definition = self._definitions[name]
        except KeyError as exc:
            available = ", ".join(sorted(self._definitions)) or "none"
            raise ValueError(
                f"Unknown {self.component_kind}: {name}. Available: {available}"
            ) from exc

        factory = self._resolve(definition)
        return factory(**kwargs)

    @staticmethod
    def _resolve(definition: ComponentDefinition) -> ComponentFactory:
        if not isinstance(definition, str):
            return definition

        module_name, separator, attribute_name = definition.partition(":")
        if not separator:
            module_name, separator, attribute_name = definition.rpartition(".")
        if not module_name or not separator or not attribute_name:
            raise ValueError(
                f"Invalid component import path '{definition}'. "
                "Use 'package.module:ClassName'."
            )

        return getattr(import_module(module_name), attribute_name)

    def __getitem__(self, name: str) -> ComponentFactory:
        return self._resolve(self._definitions[name])

    def __iter__(self) -> Iterator[str]:
        return iter(self._definitions)

    def __len__(self) -> int:
        return len(self._definitions)
