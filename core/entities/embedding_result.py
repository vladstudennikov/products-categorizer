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
