from core.abstractions.accessor import BaseAccessor
from core.entities.product import Product


class ProductAccessor(BaseAccessor[Product]):
    def get_text(self, entity: Product) -> str:
        """Returns only the name as description was removed from base Product."""
        return entity.name

    def get_id(self, entity: Product) -> str:
        return entity.id
