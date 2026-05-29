from core.abstractions.adapter import BaseAdapter
from core.entities.product import Product


class ExcelProductAdapter(BaseAdapter):
    def transform(self, dataframe):
        products = []

        for _, row in dataframe.iterrows():
            products.append(
                Product(
                    id=str(row["id"]),
                    name=row["name"]
                )
            )

        return products
