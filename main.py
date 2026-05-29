from core.context.pipeline_context import PipelineContext
from core.context.persistent_pipeline_context import PersistentPipelineContext
from core.operations.clustering_operation import ClusteringOperation
from core.operations.vectorization_operation import VectorizationOperation
from core.operations.validation_operation import ValidationOperation
from core.operations.persistence_operation import StatePersistenceOperation
from core.pipeline.iterative_executor import IterativeExecutor
from core.pipeline.nodes import ActionNode

from core.factories.clusterizer_factory import ClusterizerFactory
from core.factories.vectorizer_factory import VectorizerFactory
from core.factories.validator_factory import ValidatorFactory

from core.services.config_service import ConfigService
from implementations.adapters.excel_product_adapter import ExcelProductAdapter


# 1. Load ALL configurations
vectorizer_config = ConfigService.load("configs/vectorizers.yaml")
clusterizer_config = ConfigService.load("configs/clusterizers.yaml")
validator_config = ConfigService.load("configs/validators.yaml")
pipeline_config = ConfigService.load("configs/pipeline.yaml")


# 2. Setup Components
vectorizer = VectorizerFactory.create(
    vectorizer_config["vectorizer"]["name"],
    **vectorizer_config["vectorizer"]["params"]
)

clusterizer = ClusterizerFactory.create(
    clusterizer_config["clusterizer"]["name"],
    **clusterizer_config["clusterizer"]["params"]
)

adapter = ExcelProductAdapter()

# 3. Setup Validators
def create_validators(config_list):
    return [
        ValidatorFactory.create(v["name"], **v["params"])
        for v in config_list
    ]

vectorization_validators = create_validators(
    validator_config["validators"]["vectorization"]
)


# 4. Create Operations
vectorization_validation_op = ValidationOperation(vectorization_validators)
vectorization_op = VectorizationOperation(vectorizer)
clustering_op = ClusteringOperation(clusterizer)