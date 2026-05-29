# Extension Guide: How to scale the Kernel

This guide explains how to add new components to the AI Marketing Analytics Kernel.

---

## 1. Adding a New Validator
**Scenario:** You want to add a `DensityValidator` for clustering results.

1. **Create the Logic:**
   Create `implementations/validators/density_validator.py`:
   ```python
   from core.abstractions.validator import BaseValidator
   class DensityValidator(BaseValidator):
       def __init__(self, min_density: float):
           self.min_density = min_density
       def validate(self, data):
           if data.clusters and data.clusters.density < self.min_density:
               raise ValueError("Cluster density too low!")
   ```

2. **Register it:**
   Add to `core/registries/validator_registry.py`:
   ```python
   from implementations.validators.density_validator import DensityValidator
   VALIDATORS["density"] = DensityValidator
   ```

3. **Configure it:**
   Add to `configs/validators.yaml`:
   ```yaml
   clustering:
     - name: density
       params: { min_density: 0.8 }
   ```

---

## 2. Adding a New Vectorizer
**Scenario:** You want to use TF-IDF instead of Transformers.

1. **Create the Logic:**
   Create `implementations/vectorizers/tfidf_vectorizer.py`:
   ```python
   from core.abstractions.vectorizer import BaseVectorizer
   from core.entities.embedding_result import EmbeddingResult
   class TfidfVectorizer(BaseVectorizer):
       def vectorize(self, products):
           # ... implementation using sklearn ...
           return EmbeddingResult(...)
   ```

2. **Register it:**
   Add to `core/registries/vectorizer_registry.py`:
   ```python
   VECTORIZERS["tfidf"] = TfidfVectorizer
   ```

3. **Configure it:**
   Update `configs/vectorizers.yaml`:
   ```yaml
   vectorizer:
     name: tfidf
     params: { max_features: 500 }
   ```

---

## 3. Adding a New Pipeline Operation
**Scenario:** You want to add a "Data Cleaning" step before vectorization.

1. **Create the Operation:**
   Create `core/operations/cleaning_operation.py`:
   ```python
   from core.abstractions.operation import BaseOperation
   class CleaningOperation(BaseOperation):
       def run(self, context):
           for p in context.state.products:
               p.name = p.name.strip().lower()
   ```

2. **Add to Pipeline:**
   In `main.py`:
   ```python
   clean_op = CleaningOperation()
   clean_node = ActionNode("clean", clean_op)
   
   # Wire it in
   clean_node.connect(vectorize_node)
   # Update executor to start at clean_node
   executor.execute(clean_node, context)
   ```

---

## Summary of the Pattern
For almost any new feature:
1. **Implement** (in `implementations/`)
2. **Register** (in `core/registries/`)
3. **Configure** (in `configs/`)
