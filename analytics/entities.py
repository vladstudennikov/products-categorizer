from pydantic import BaseModel

class AnalyticsProduct(BaseModel):
    id: str
    name: str
    price: float
