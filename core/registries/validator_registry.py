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
