from core.abstractions.accessor import BaseAccessor
from analytics.entities import AnalyticsProduct

class AnalyticsProductAccessor(BaseAccessor[AnalyticsProduct]):
    def get_text(self, entity: AnalyticsProduct) -> str:
        return entity.name

    def get_id(self, entity: AnalyticsProduct) -> str:
        return entity.id
