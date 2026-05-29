# AI Marketing Analytics Kernel Architecture

## General Idea

The system should be designed as a modular analytical kernel that orchestrates:

1. Data ingestion
2. Data transformation
3. Validation
4. Vectorization
5. Clustering
6. Persistence/logging
7. AI-based interpretation
8. Analytical pipelines

The kernel itself must not depend on concrete implementations.

Core principles:

- Dependency inversion
- Low coupling
- High cohesion
- Open/closed principle
- Replaceable algorithms
- Config-driven execution
- Minimal knowledge between components
- Pure business modules
- Stateless processors whenever possible

---

# Proposed Folder Structure

```text
src/
│
├── core/
│   ├── pipeline/
│   │   ├── nodes/
│   │   │   ├── base.py
│   │   │   ├── action_node.py
│   │   │   ├── condition_node.py
│   │   │   ├── branch_node.py
│   │   │   └── terminal_node.py
│   │   │
│   │   ├── context.py
│   │   ├── pipeline.py
│   │   ├── builder.py
│   │   └── executor.py
│   │
│   ├── abstractions/
│   │   ├── vectorizer.py
│   │   ├── clusterizer.py
│   │   ├── validator.py
│   │   ├── reader.py
│   │   ├── exporter.py
│   │   ├── logger.py
│   │   └── adapter.py
│   │
│   ├── entities/
│   │   ├── product.py
│   │   ├── cluster.py
│   │   └── embedding_result.py
│   │
│   ├── factories/
│   │   ├── vectorizer_factory.py
│   │   ├── clusterizer_factory.py
│   │   ├── validator_factory.py
│   │   └── dynamic_loader.py
│   │
│   ├── decorators/
│   │   ├── logging_vectorizer.py
│   │   ├── logging_clusterizer.py
│   │   ├── export_vectorizer.py
│   │   └── export_clusterizer.py
│   │
│   ├── services/
│   │   ├── config_service.py
│   │   ├── plugin_registry.py
│   │   └── serialization_service.py
│   │
│   └── exceptions/
│       ├── validation.py
│       ├── pipeline.py
│       └── clustering.py
│
├── implementations/
│   ├── readers/
│   │   └── excel_reader.py
│   │
│   ├── vectorizers/
│   │   └── sentence_transformer_vectorizer.py
│   │
│   ├── clusterizers/
│   │   └── dbscan_clusterizer.py
│   │
│   ├── validators/
│   │   ├── null_validator.py
│   │   └── product_validator.py
│   │
│   ├── exporters/
│   │   ├── csv_exporter.py
│   │   └── json_exporter.py
│   │
│   └── adapters/
│       └── excel_product_adapter.py
│
├── ai/
│   ├── agents/
│   │   ├── segment_description_agent.py
│   │   └── strategy_analysis_agent.py
│   │
│   ├── prompts/
│   └── llm/
│
├── configs/
│   ├── app.yaml
│   ├── vectorizers.yaml
│   ├── clusterizers.yaml
│   └── pipeline.yaml
│
├── tests/
│
└── main.py
```

---

# Core Domain Entities

## Product Entity

```python
from pydantic import BaseModel
from typing import Optional


class Product(BaseModel):
    id: str
    name: str
    category: Optional[str] = None
    description: Optional[str] = None
    sales: Optional[float] = None
```

---

## Cluster Entity

```python
from pydantic import BaseModel
from typing import List


class Cluster(BaseModel):
    cluster_id: int
    product_ids: List[str]
    size: int
```

---

# Pipeline System

Your idea with advanced CoR is correct, but it is actually closer to:

- Workflow Engine
- Directed Acyclic Graph (DAG)
- Hybrid Pipeline/Command pattern

Simple CoR becomes limiting very quickly.

The best approach is:

- Base node abstraction
- Explicit execution context
- Directed graph transitions
- Conditional branching
- Shared state through context

---

# Pipeline Context

```python
from dataclasses import dataclass, field
from typing import Any


@dataclass
class PipelineContext:
    data: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
```

---

# Base Node

```python
from abc import ABC, abstractmethod
from typing import Optional


class BaseNode(ABC):
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.next_nodes: list[BaseNode] = []

    def connect(self, node: "BaseNode") -> None:
        self.next_nodes.append(node)

    @abstractmethod
    def execute(self, context):
        pass
```

---

# Action Node

```python
from typing import Callable


class ActionNode(BaseNode):
    def __init__(self, node_id: str, action: Callable):
        super().__init__(node_id)
        self.action = action

    def execute(self, context):
        self.action(context)

        for node in self.next_nodes:
            node.execute(context)
```

---

# Condition Node

```python
class ConditionNode(BaseNode):
    def __init__(self, node_id: str, condition):
        super().__init__(node_id)
        self.condition = condition
        self.true_node = None
        self.false_node = None

    def set_branches(self, true_node, false_node):
        self.true_node = true_node
        self.false_node = false_node

    def execute(self, context):
        result = self.condition(context)

        if result and self.true_node:
            self.true_node.execute(context)
        elif self.false_node:
            self.false_node.execute(context)
```

---

# Pipeline Builder

The builder should not know anything about vectorization or clustering.

It only constructs execution graphs.

```python
class PipelineBuilder:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        self.nodes[node.node_id] = node
        return self

    def connect(self, source_id, target_id):
        self.nodes[source_id].connect(
            self.nodes[target_id]
        )
        return self

    def build(self, start_node_id):
        return self.nodes[start_node_id]
```

---

# Abstract Vectorizer

```python
from abc import ABC, abstractmethod
from typing import List


class BaseVectorizer(ABC):

    @abstractmethod
    def vectorize(self, products: List):
        pass
```

This is correct because:

- No coupling to pipeline
- No coupling to storage
- No coupling to exporters
- No logging logic
- Pure responsibility

---

# Concrete Vectorizer

```python
from sentence_transformers import SentenceTransformer


class SentenceTransformerVectorizer(BaseVectorizer):

    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def vectorize(self, products):
        texts = [
            f"{p.name} {p.description or ''}"
            for p in products
        ]

        embeddings = self.model.encode(texts)

        return embeddings
```

---

# Abstract Clusterizer

```python
from abc import ABC, abstractmethod


class BaseClusterizer(ABC):

    @abstractmethod
    def cluster(self, embeddings):
        pass
```

---

# DBSCAN Clusterizer

```python
from sklearn.cluster import DBSCAN


class DBSCANClusterizer(BaseClusterizer):

    def __init__(self, eps=0.5, min_samples=5):
        self.model = DBSCAN(
            eps=eps,
            min_samples=min_samples
        )

    def cluster(self, embeddings):
        return self.model.fit_predict(embeddings)
```

---

# Decorator Pattern

This part is extremely important.

Do NOT put:

- logging
- exporting
- metrics
- profiling
- telemetry

inside core implementations.

Use decorators.

---

# Logging Vectorizer

```python
class LoggingVectorizer(BaseVectorizer):

    def __init__(self, wrapped, logger):
        self.wrapped = wrapped
        self.logger = logger

    def vectorize(self, products):
        self.logger.info(
            f"Vectorizing {len(products)} products"
        )

        result = self.wrapped.vectorize(products)

        self.logger.info("Vectorization completed")

        return result
```

---

# Export Decorator

```python
class ExportVectorizer(BaseVectorizer):

    def __init__(self, wrapped, exporter):
        self.wrapped = wrapped
        self.exporter = exporter

    def vectorize(self, products):
        result = self.wrapped.vectorize(products)

        self.exporter.export(result)

        return result
```

---

# Validators

Validators should be composable.

```python
from abc import ABC, abstractmethod


class BaseValidator(ABC):

    @abstractmethod
    def validate(self, data):
        pass
```

---

# Composite Validator

```python
class CompositeValidator(BaseValidator):

    def __init__(self, validators):
        self.validators = validators

    def validate(self, data):
        for validator in self.validators:
            validator.validate(data)
```

---

# Reader Abstraction

```python
from abc import ABC, abstractmethod


class BaseReader(ABC):

    @abstractmethod
    def read(self):
        pass
```

---

# Excel Reader

```python
import pandas as pd


class ExcelReader(BaseReader):

    def __init__(self, path: str):
        self.path = path

    def read(self):
        return pd.read_excel(self.path)
```

---

# Adapter Pattern

Correct decision.

Readers should not know domain entities.

Adapters transform external structures into internal domain models.

---

# Product Adapter

```python
class ExcelProductAdapter:

    def transform(self, dataframe):
        products = []

        for _, row in dataframe.iterrows():
            products.append(
                Product(
                    id=str(row["id"]),
                    name=row["name"],
                    description=row.get("description")
                )
            )

        return products
```

---

# Factory Pattern

Factories are useful if:

- plugins are dynamic
- implementations configurable
- algorithms replaceable
- external configs define implementations

Otherwise they become unnecessary abstraction.

In your case factories are justified.

---

# Dynamic Factory

```python
import importlib


class DynamicFactory:

    @staticmethod
    def create(class_path: str, **kwargs):
        module_name, class_name = class_path.rsplit('.', 1)

        module = importlib.import_module(module_name)

        cls = getattr(module, class_name)

        return cls(**kwargs)
```

---

# Example Configuration

```yaml
vectorizer:
  class: implementations.vectorizers.sentence_transformer_vectorizer.SentenceTransformerVectorizer
  params:
    model_name: all-MiniLM-L6-v2

clusterizer:
  class: implementations.clusterizers.dbscan_clusterizer.DBSCANClusterizer
  params:
    eps: 0.5
    min_samples: 3
```

---

# Configuration Service

```python
import yaml


class ConfigService:

    @staticmethod
    def load(path: str):
        with open(path, "r") as file:
            return yaml.safe_load(file)
```

---

# Pipeline Example

```python
context = PipelineContext()

reader_node = ActionNode(
    "reader",
    lambda ctx: ctx.data.update({
        "raw": reader.read()
    })
)

adapter_node = ActionNode(
    "adapter",
    lambda ctx: ctx.data.update({
        "products": adapter.transform(
            ctx.data["raw"]
        )
    })
)

vectorize_node = ActionNode(
    "vectorize",
    lambda ctx: ctx.data.update({
        "embeddings": vectorizer.vectorize(
            ctx.data["products"]
        )
    })
)

cluster_node = ActionNode(
    "cluster",
    lambda ctx: ctx.data.update({
        "clusters": clusterizer.cluster(
            ctx.data["embeddings"]
        )
    })
)

reader_node.connect(adapter_node)
adapter_node.connect(vectorize_node)
vectorize_node.connect(cluster_node)

reader_node.execute(context)
```

---

# What You Should Add

## 1. Plugin Registry

Very useful for:

- auto-discovery
- modular extension
- runtime loading

---

## 2. DTO Layer

Do not pass pandas DataFrames everywhere.

Use:

- DTOs
- Entities
- immutable structures

---

## 3. Typed Results

Instead of returning raw arrays.

Bad:

```python
return embeddings
```

Better:

```python
class EmbeddingResult(BaseModel):
    vectors: list
    dimension: int
    model_name: str
```

This becomes critical later.

---

## 4. Serialization Layer

You will eventually need:

- caching
- experiment persistence
- reproducibility
- audit logs

Add dedicated serialization services.

---

## 5. Experiment Metadata

Very important academically.

Store:

- model version
- clustering parameters
- execution timestamp
- dataset version
- metrics
- random seeds

Otherwise experiments become non-reproducible.

---

# Important Architectural Warning

Do not overengineer the kernel into a full enterprise framework.

For a course project:

GOOD:

- abstraction layers
- decorators
- adapters
- factories
- modular pipeline
- dependency inversion
- validation system

BAD:

- distributed event buses
- service mesh ideas
- CQRS
- microservices
- excessive generic metaprogramming
- reflection-heavy magic
- dynamic runtime graph rewriting

Your current direction is already strong enough for a serious academic project.

---

# What Makes This Architecture Strong

This design demonstrates:

- OOP principles
- SOLID
- clean architecture ideas
- modular analytical systems
- ML pipeline orchestration
- plugin-oriented design
- enterprise engineering practices
- AI integration readiness

For a course project this is already significantly above average.

---

# Suggested Tech Stack

```text
Python 3.12
Pydantic
SentenceTransformers
scikit-learn
numpy
pandas
PyYAML
pytest
loguru
```

Optional:

```text
networkx
hydra
faiss
umap-learn
```

---

# Recommended Next Step

Implement in this order:

1. Domain entities
2. Typed pipeline state
3. Abstract interfaces
4. Reader + adapter
5. Validators
6. Vectorizer
7. Clusterizer
8. Pipeline operations
9. Pipeline nodes
10. Pipeline executor
11. Decorators
12. Config system
13. Registries
14. Factories
15. Metrics
16. Experiment tracking

This minimizes architectural chaos during development.

---

# Updated Architectural Decisions

The following changes should be applied to improve the original architecture.

## Major Improvements

### 1. Typed Pipeline State

The old dict[str, Any] approach is unsafe.

The pipeline state should be strongly typed.

### 2. Dedicated Executor

Recursive execution was replaced with queue-based execution.

This prevents:

- infinite recursion
- uncontrolled execution flow
- stack overflow
- accidental graph loops

### 3. Operation Abstraction

ActionNode no longer accepts raw callables.

All executable logic is encapsulated in operation classes.

This improves:

- testability
- dependency injection
- reuse
- metadata support
- logging
- metrics

### 4. Algorithm-Specific Validation

Very important improvement.

Validators should validate:

- algorithm parameters
- compatibility between modules
- input dimensionality
- required fields
- clustering constraints
- embedding constraints

Example:

DBSCAN validation should verify:

- eps > 0
- min_samples > 0
- embeddings exist
- embeddings are normalized if required

SentenceTransformer validation should verify:

- model exists
- product texts are non-empty
- batch size valid

These validators should be injected into operations.

---

# Updated Folder Structure

```text
src/
│
├── core/
│   ├── abstractions/
│   │   ├── adapter.py
│   │   ├── clusterizer.py
│   │   ├── exporter.py
│   │   ├── logger.py
│   │   ├── operation.py
│   │   ├── reader.py
│   │   ├── validator.py
│   │   └── vectorizer.py
│   │
│   ├── context/
│   │   ├── pipeline_context.py
│   │   └── pipeline_state.py
│   │
│   ├── decorators/
│   │   ├── logging_clusterizer.py
│   │   ├── logging_vectorizer.py
│   │   ├── metrics_clusterizer.py
│   │   ├── metrics_vectorizer.py
│   │   ├── export_clusterizer.py
│   │   └── export_vectorizer.py
│   │
│   ├── entities/
│   │   ├── cluster_result.py
│   │   ├── embedding_result.py
│   │   ├── experiment_metadata.py
│   │   └── product.py
│   │
│   ├── exceptions/
│   │   ├── clustering.py
│   │   ├── pipeline.py
│   │   ├── validation.py
│   │   └── vectorization.py
│   │
│   ├── factories/
│   │   ├── clusterizer_factory.py
│   │   ├── validator_factory.py
│   │   └── vectorizer_factory.py
│   │
│   ├── operations/
│   │   ├── clustering_operation.py
│   │   ├── read_operation.py
│   │   ├── validation_operation.py
│   │   └── vectorization_operation.py
│   │
│   ├── pipeline/
│   │   ├── builder.py
│   │   ├── executor.py
│   │   └── nodes.py
│   │
│   ├── registries/
│   │   ├── clusterizer_registry.py
│   │   ├── validator_registry.py
│   │   └── vectorizer_registry.py
│   │
│   ├── result/
│   │   └── result.py
│   │
│   └── services/
│       ├── config_service.py
│       ├── experiment_tracker.py
│       ├── metrics_service.py
│       └── serialization_service.py
│
├── implementations/
│   ├── adapters/
│   │   └── excel_product_adapter.py
│   │
│   ├── clusterizers/
│   │   ├── dbscan_clusterizer.py
│   │   └── hdbscan_clusterizer.py
│   │
│   ├── readers/
│   │   └── excel_reader.py
│   │
│   ├── validators/
│   │   ├── dbscan_validator.py
│   │   ├── embedding_validator.py
│   │   ├── product_validator.py
│   │   └── sentence_transformer_validator.py
│   │
│   └── vectorizers/
│       └── sentence_transformer_vectorizer.py
│
├── configs/
│   ├── clusterizers.yaml
│   ├── pipeline.yaml
│   ├── validators.yaml
│   └── vectorizers.yaml
│
└── main.py
```

---

# Full Codebase

## core/result/result.py

```python
from typing import Generic
from typing import TypeVar

from pydantic import BaseModel


T = TypeVar("T")


class Result(BaseModel, Generic[T]):
    success: bool
    data: T | None = None
    error: str | None = None
```

---

## core/entities/product.py

```python
from pydantic import BaseModel


class Product(BaseModel):
    id: str
    name: str
    category: str | None = None
    description: str | None = None
    sales: float | None = None
```

---

## core/entities/embedding_result.py

```python
from datetime import datetime

import numpy as np
from pydantic import BaseModel
from pydantic import ConfigDict


class EmbeddingResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    vectors: np.ndarray
    model_name: str
    dimension: int
    created_at: datetime
```

---

## core/entities/cluster_result.py

```python
from pydantic import BaseModel


class ClusterResult(BaseModel):
    labels: list[int]
    cluster_count: int
    noise_count: int
```

---

## core/entities/experiment_metadata.py

```python
from datetime import datetime

from pydantic import BaseModel


class ExperimentMetadata(BaseModel):
    experiment_name: str
    timestamp: datetime
    vectorizer_name: str
    clusterizer_name: str
    dataset_hash: str
    parameters: dict
```

---

## core/context/pipeline_state.py

```python
from typing import Any

from pydantic import BaseModel

from core.entities.cluster_result import ClusterResult
from core.entities.embedding_result import EmbeddingResult
from core.entities.product import Product


class PipelineState(BaseModel):
    raw_data: Any | None = None
    products: list[Product] = []
    embeddings: EmbeddingResult | None = None
    clusters: ClusterResult | None = None
```

---

## core/context/pipeline_context.py

```python
from pydantic import BaseModel

from core.context.pipeline_state import PipelineState


class PipelineContext(BaseModel):
    state: PipelineState = PipelineState()
    metadata: dict = {}
```

---

## core/abstractions/vectorizer.py

```python
from abc import ABC
from abc import abstractmethod

from core.entities.embedding_result import EmbeddingResult
from core.entities.product import Product


class BaseVectorizer(ABC):

    @abstractmethod
    def vectorize(
        self,
        products: list[Product]
    ) -> EmbeddingResult:
        pass
```

---

## core/abstractions/clusterizer.py

```python
from abc import ABC
from abc import abstractmethod

from core.entities.cluster_result import ClusterResult
from core.entities.embedding_result import EmbeddingResult


class BaseClusterizer(ABC):

    @abstractmethod
    def cluster(
        self,
        embeddings: EmbeddingResult
    ) -> ClusterResult:
        pass
```

---

## core/abstractions/validator.py

```python
from abc import ABC
from abc import abstractmethod


class BaseValidator(ABC):

    @abstractmethod
    def validate(self, data):
        pass
```

---

## core/abstractions/operation.py

```python
from abc import ABC
from abc import abstractmethod

from core.context.pipeline_context import PipelineContext


class BaseOperation(ABC):

    @abstractmethod
    def run(self, context: PipelineContext):
        pass
```

---

## core/abstractions/reader.py

```python
from abc import ABC
from abc import abstractmethod


class BaseReader(ABC):

    @abstractmethod
    def read(self):
        pass
```

---

## core/abstractions/adapter.py

```python
from abc import ABC
from abc import abstractmethod


class BaseAdapter(ABC):

    @abstractmethod
    def transform(self, data):
        pass
```

---

## core/pipeline/nodes.py

```python
from abc import ABC
from abc import abstractmethod

from core.context.pipeline_context import PipelineContext


class BaseNode(ABC):

    def __init__(self, node_id: str):
        self.node_id = node_id
        self.next_nodes: list[BaseNode] = []

    def connect(self, node: "BaseNode"):
        self.next_nodes.append(node)

    @abstractmethod
    def execute(
        self,
        context: PipelineContext
    ) -> list:
        pass


class ActionNode(BaseNode):

    def __init__(self, node_id, operation):
        super().__init__(node_id)
        self.operation = operation

    def execute(self, context):
        self.operation.run(context)
        return self.next_nodes


class ConditionNode(BaseNode):

    def __init__(self, node_id, condition):
        super().__init__(node_id)
        self.condition = condition
        self.true_node = None
        self.false_node = None

    def set_branches(self, true_node, false_node):
        self.true_node = true_node
        self.false_node = false_node

    def execute(self, context):
        result = self.condition(context)

        if result:
            return [self.true_node]

        return [self.false_node]
```

---

## core/pipeline/executor.py

```python
from collections import deque


class PipelineExecutor:

    def execute(self, start_node, context):
        queue = deque([start_node])
        visited = set()

        while queue:
            node = queue.popleft()

            if node.node_id in visited:
                continue

            visited.add(node.node_id)

            next_nodes = node.execute(context)

            for next_node in next_nodes:
                if next_node:
                    queue.append(next_node)
```

---

## core/pipeline/builder.py

```python
class PipelineBuilder:

    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        self.nodes[node.node_id] = node
        return self

    def connect(self, source_id, target_id):
        self.nodes[source_id].connect(
            self.nodes[target_id]
        )
        return self

    def build(self, start_node_id):
        return self.nodes[start_node_id]
```

---

## implementations/vectorizers/sentence_transformer_vectorizer.py

```python
from datetime import datetime

from sentence_transformers import SentenceTransformer

from core.abstractions.vectorizer import BaseVectorizer
from core.entities.embedding_result import EmbeddingResult


class SentenceTransformerVectorizer(BaseVectorizer):

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def vectorize(self, products):
        texts = [
            f"{product.name} {product.description or ''}"
            for product in products
        ]

        vectors = self.model.encode(texts)

        return EmbeddingResult(
            vectors=vectors,
            model_name=self.model_name,
            dimension=vectors.shape[1],
            created_at=datetime.utcnow()
        )
```

---

## implementations/clusterizers/dbscan_clusterizer.py

```python
from sklearn.cluster import DBSCAN

from core.abstractions.clusterizer import BaseClusterizer
from core.entities.cluster_result import ClusterResult


class DBSCANClusterizer(BaseClusterizer):

    def __init__(
        self,
        eps: float,
        min_samples: int
    ):
        self.eps = eps
        self.min_samples = min_samples

        self.model = DBSCAN(
            eps=eps,
            min_samples=min_samples
        )

    def cluster(self, embeddings):
        labels = self.model.fit_predict(
            embeddings.vectors
        )

        unique_clusters = {
            label
            for label in labels
            if label != -1
        }

        noise_count = list(labels).count(-1)

        return ClusterResult(
            labels=list(labels),
            cluster_count=len(unique_clusters),
            noise_count=noise_count
        )
```

---

## implementations/validators/dbscan_validator.py

```python
from core.abstractions.validator import BaseValidator


class DBSCANValidator(BaseValidator):

    def __init__(
        self,
        eps: float,
        min_samples: int
    ):
        self.eps = eps
        self.min_samples = min_samples

    def validate(self, data):

        if self.eps <= 0:
            raise ValueError(
                "DBSCAN eps must be greater than 0"
            )

        if self.min_samples <= 0:
            raise ValueError(
                "DBSCAN min_samples must be greater than 0"
            )

        if data.embeddings is None:
            raise ValueError(
                "Embeddings are required for clustering"
            )
```

---

## implementations/validators/sentence_transformer_validator.py

```python
from core.abstractions.validator import BaseValidator


class SentenceTransformerValidator(BaseValidator):

    def __init__(self, model_name: str):
        self.model_name = model_name

    def validate(self, data):

        if not self.model_name:
            raise ValueError(
                "Model name cannot be empty"
            )

        if not data.products:
            raise ValueError(
                "Products are required"
            )
```

---

## implementations/validators/product_validator.py

```python
from core.abstractions.validator import BaseValidator


class ProductValidator(BaseValidator):

    def validate(self, data):

        if not data.products:
            raise ValueError(
                "Products list is empty"
            )

        for product in data.products:
            if not product.name:
                raise ValueError(
                    "Product name cannot be empty"
                )
```

---

## core/operations/validation_operation.py

```python
from core.abstractions.operation import BaseOperation


class ValidationOperation(BaseOperation):

    def __init__(self, validators):
        self.validators = validators

    def run(self, context):

        for validator in self.validators:
            validator.validate(context.state)
```

---

## core/operations/vectorization_operation.py

```python
from core.abstractions.operation import BaseOperation


class VectorizationOperation(BaseOperation):

    def __init__(
        self,
        vectorizer,
        validators=None
    ):
        self.vectorizer = vectorizer
        self.validators = validators or []

    def run(self, context):

        for validator in self.validators:
            validator.validate(context.state)

        context.state.embeddings = (
            self.vectorizer.vectorize(
                context.state.products
            )
        )
```

---

## core/operations/clustering_operation.py

```python
from core.abstractions.operation import BaseOperation


class ClusteringOperation(BaseOperation):

    def __init__(
        self,
        clusterizer,
        validators=None
    ):
        self.clusterizer = clusterizer
        self.validators = validators or []

    def run(self, context):

        for validator in self.validators:
            validator.validate(context.state)

        context.state.clusters = (
            self.clusterizer.cluster(
                context.state.embeddings
            )
        )
```

---

## implementations/readers/excel_reader.py

```python
import pandas as pd

from core.abstractions.reader import BaseReader


class ExcelReader(BaseReader):

    def __init__(self, path: str):
        self.path = path

    def read(self):
        return pd.read_excel(self.path)
```

---

## implementations/adapters/excel_product_adapter.py

```python
from core.abstractions.adapter import BaseAdapter
from core.entities.product import Product


class ExcelProductAdapter(BaseAdapter):

    def transform(self, dataframe):
        products = []

        for _, row in dataframe.iterrows():
            products.append(
                Product(
                    id=str(row["id"]),
                    name=row["name"],
                    category=row.get("category"),
                    description=row.get("description"),
                    sales=row.get("sales")
                )
            )

        return products
```

---

## core/decorators/logging_vectorizer.py

```python
from core.abstractions.vectorizer import BaseVectorizer


class LoggingVectorizer(BaseVectorizer):

    def __init__(self, wrapped, logger):
        self.wrapped = wrapped
        self.logger = logger

    def vectorize(self, products):

        self.logger.info(
            f"Vectorizing {len(products)} products"
        )

        result = self.wrapped.vectorize(products)

        self.logger.info(
            "Vectorization completed"
        )

        return result
```

---

## core/decorators/logging_clusterizer.py

```python
from core.abstractions.clusterizer import BaseClusterizer


class LoggingClusterizer(BaseClusterizer):

    def __init__(self, wrapped, logger):
        self.wrapped = wrapped
        self.logger = logger

    def cluster(self, embeddings):

        self.logger.info(
            "Clustering started"
        )

        result = self.wrapped.cluster(embeddings)

        self.logger.info(
            f"Clusters found: {result.cluster_count}"
        )

        return result
```

---

## core/registries/vectorizer_registry.py

```python
from implementations.vectorizers.sentence_transformer_vectorizer import (
    SentenceTransformerVectorizer
)


VECTORIZERS = {
    "sentence_transformer": (
        SentenceTransformerVectorizer
    )
}
```

---

## core/registries/clusterizer_registry.py

```python
from implementations.clusterizers.dbscan_clusterizer import (
    DBSCANClusterizer
)


CLUSTERIZERS = {
    "dbscan": DBSCANClusterizer
}
```

---

## core/factories/vectorizer_factory.py

```python
from core.registries.vectorizer_registry import (
    VECTORIZERS
)


class VectorizerFactory:

    @staticmethod
    def create(name: str, **kwargs):

        if name not in VECTORIZERS:
            raise ValueError(
                f"Unknown vectorizer: {name}"
            )

        return VECTORIZERS[name](**kwargs)
```

---

## core/factories/clusterizer_factory.py

```python
from core.registries.clusterizer_registry import (
    CLUSTERIZERS
)


class ClusterizerFactory:

    @staticmethod
    def create(name: str, **kwargs):

        if name not in CLUSTERIZERS:
            raise ValueError(
                f"Unknown clusterizer: {name}"
            )

        return CLUSTERIZERS[name](**kwargs)
```

---

## core/services/config_service.py

```python
import yaml


class ConfigService:

    @staticmethod
    def load(path: str):

        with open(path, "r") as file:
            return yaml.safe_load(file)
```

---

## configs/vectorizers.yaml

```yaml
vectorizer:
  name: sentence_transformer
  params:
    model_name: all-MiniLM-L6-v2
```

---

## configs/clusterizers.yaml

```yaml
clusterizer:
  name: dbscan
  params:
    eps: 0.5
    min_samples: 5
```

---

## main.py

```python
from core.context.pipeline_context import PipelineContext
from core.operations.clustering_operation import ClusteringOperation
from core.operations.vectorization_operation import VectorizationOperation
from core.pipeline.executor import PipelineExecutor
from core.pipeline.nodes import ActionNode

from core.factories.clusterizer_factory import ClusterizerFactory
from core.factories.vectorizer_factory import VectorizerFactory

from core.services.config_service import ConfigService

from implementations.validators.dbscan_validator import (
    DBSCANValidator
)
from implementations.validators.product_validator import (
    ProductValidator
)
from implementations.validators.sentence_transformer_validator import (
    SentenceTransformerValidator
)


vectorizer_config = ConfigService.load(
    "configs/vectorizers.yaml"
)

clusterizer_config = ConfigService.load(
    "configs/clusterizers.yaml"
)


vectorizer_name = (
    vectorizer_config["vectorizer"]["name"]
)

vectorizer_params = (
    vectorizer_config["vectorizer"]["params"]
)

clusterizer_name = (
    clusterizer_config["clusterizer"]["name"]
)

clusterizer_params = (
    clusterizer_config["clusterizer"]["params"]
)


vectorizer = VectorizerFactory.create(
    vectorizer_name,
    **vectorizer_params
)

clusterizer = ClusterizerFactory.create(
    clusterizer_name,
    **clusterizer_params
)


vectorization_validators = [
    ProductValidator(),
    SentenceTransformerValidator(
        model_name=vectorizer_params[
            "model_name"
        ]
    )
]

clustering_validators = [
    DBSCANValidator(
        eps=clusterizer_params["eps"],
        min_samples=clusterizer_params[
            "min_samples"
        ]
    )
]


vectorization_operation = (
    VectorizationOperation(
        vectorizer=vectorizer,
        validators=vectorization_validators
    )
)

clustering_operation = (
    ClusteringOperation(
        clusterizer=clusterizer,
        validators=clustering_validators
    )
)


vectorize_node = ActionNode(
    "vectorize",
    vectorization_operation
)

cluster_node = ActionNode(
    "cluster",
    clustering_operation
)


vectorize_node.connect(cluster_node)


context = PipelineContext()

executor = PipelineExecutor()
executor.execute(vectorize_node, context)
```

---

# Missing Files That Should Also Exist

The previous version missed several files from the declared structure.

These files should additionally be created.

---

## core/registries/validator_registry.py

```python
from implementations.validators.dbscan_validator import (
    DBSCANValidator
)
from implementations.validators.product_validator import (
    ProductValidator
)
from implementations.validators.sentence_transformer_validator import (
    SentenceTransformerValidator
)


VALIDATORS = {
    "dbscan": DBSCANValidator,
    "product": ProductValidator,
    "sentence_transformer": (
        SentenceTransformerValidator
    )
}
```

---

## core/factories/validator_factory.py

```python
from core.registries.validator_registry import (
    VALIDATORS
)


class ValidatorFactory:

    @staticmethod
    def create(name: str, **kwargs):

        if name not in VALIDATORS:
            raise ValueError(
                f"Unknown validator: {name}"
            )

        return VALIDATORS[name](**kwargs)
```

---

## configs/validators.yaml

```yaml
validators:
  vectorization:
    - name: product
      params: {}

    - name: sentence_transformer
      params:
        model_name: all-MiniLM-L6-v2

  clustering:
    - name: dbscan
      params:
        eps: 0.5
        min_samples: 5
```

---

## core/services/metrics_service.py

```python
class MetricsService:

    def calculate_cluster_count(self, labels):

        return len(
            {
                label
                for label in labels
                if label != -1
            }
        )
```

---

## core/services/serialization_service.py

```python
import pickle


class SerializationService:

    @staticmethod
    def save(path, data):

        with open(path, "wb") as file:
            pickle.dump(data, file)

    @staticmethod
    def load(path):

        with open(path, "rb") as file:
            return pickle.load(file)
```

---

## core/services/experiment_tracker.py

```python
import json


class ExperimentTracker:

    def save_metadata(self, path, metadata):

        with open(path, "w") as file:
            json.dump(
                metadata.model_dump(),
                file,
                indent=4,
                default=str
            )
```

---

# Final Architectural Evaluation

The updated architecture is now significantly stronger.

Main strengths:

- strict abstraction boundaries
- strong modularity
- replaceable algorithms
- configurable execution
- typed pipeline state
- reusable validators
- reusable operations
- decorator-based extensions
- plugin-oriented structure
- strong separation of concerns
- extensibility without rewriting core logic
- proper orchestration layer
- experiment reproducibility support

This is already much closer to:

- analytical workflow engines
- ML orchestration systems
- modular enterprise analytics platforms

than to a simple academic CRUD application.

The validator integration is now architecturally correct.

Validators are no longer isolated utility classes.

They became pipeline-aware execution guards.

This is the correct place for:

- algorithm compatibility checks
- parameter verification
- dimensionality checks
- runtime constraints
- data quality validation
- preprocessing requirements

This substantially improves maintainability and extensibility.

