import pandas as pd
import yaml
from typing import Dict, Any, List
from implementations.readers.csv_reader import CSVReader
from core.factories.vectorizer_factory import VectorizerFactory
from core.factories.clusterizer_factory import ClusterizerFactory
from analytics.entities import AnalyticsProduct
from analytics.accessors import AnalyticsProductAccessor

class AnalyticsManager:
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Use a local accessor instance for the custom entity
        self.vectorizer = VectorizerFactory.create(
            self.config['vectorizer']['name'],
            accessor=AnalyticsProductAccessor(),
            model_name=self.config['vectorizer'].get('model_name', 'all-MiniLM-L6-v2')
        )
        
        self.clusterizer = ClusterizerFactory.create(
            self.config['clusterizer']['name'],
            **{k: v for k, v in self.config['clusterizer'].items() if k != 'name'}
        )

    def get_clusters(self, products_path: str = None) -> Dict[str, List[str]]:
        """
        Performs clustering and returns a mapping of cluster_id to list of product names.
        This allows passing clusters directly to an agent.
        """
        path = products_path or self.config['data']['products_path']
        product_reader = CSVReader(path)
        df_products = product_reader.read()
        
        if df_products is None:
            raise ValueError("Could not read products data.")

        products = [
            AnalyticsProduct(id=str(row['id']), name=row['name'], price=float(row['price']))
            for _, row in df_products.iterrows()
        ]

        embeddings = self.vectorizer.vectorize(products)
        cluster_result = self.clusterizer.cluster(embeddings)
        
        # Group names by cluster ID
        clusters = {}
        for i, label in enumerate(cluster_result.labels):
            cluster_id = str(label)
            if cluster_id not in clusters:
                clusters[cluster_id] = []
            clusters[cluster_id].append(products[i].name)
            
        return clusters

    def run_analytics(self) -> pd.DataFrame:
        # 1. Load Data
        product_reader = CSVReader(self.config['data']['products_path'])
        sales_reader = CSVReader(self.config['data']['sales_path'])
        
        df_products = product_reader.read()
        df_sales = sales_reader.read()
        
        if df_products is None or df_sales is None:
            raise ValueError("Could not read data from provided paths.")

        # 2. Convert to AnalyticsProduct entities
        products = [
            AnalyticsProduct(id=str(row['id']), name=row['name'], price=float(row['price']))
            for _, row in df_products.iterrows()
        ]

        # 3. Vectorize and Clusterize
        embeddings = self.vectorizer.vectorize(products)
        cluster_result = self.clusterizer.cluster(embeddings)
        
        # 4. Map Clusters back to Products
        product_id_to_cluster = {
            products[i].id: label
            for i, label in enumerate(cluster_result.labels)
        }
        
        df_products['cluster'] = df_products['id'].astype(str).map(product_id_to_cluster)

        # 5. Merge with Sales and Compute Statistics
        df_merged = pd.merge(df_sales, df_products, left_on='product_id', right_on='id')
        df_merged['total_sum'] = df_merged['quantity'] * df_merged['price']

        # Group by cluster
        cluster_stats = df_merged.groupby('cluster').agg({
            'quantity': 'sum',
            'total_sum': 'sum',
            'price': 'mean',
            'product_id': 'nunique'
        }).rename(columns={
            'quantity': 'total_quantity_sold',
            'total_sum': 'total_revenue',
            'price': 'mean_product_price',
            'product_id': 'unique_products_in_cluster'
        })

        cluster_members = df_products.groupby('cluster')['name'].apply(lambda x: list(x)[:3]).to_frame('sample_products')
        final_stats = cluster_stats.join(cluster_members)
        
        return final_stats

if __name__ == "__main__":
    manager = AnalyticsManager("analytics/analytics_config.yaml")
    results = manager.run_analytics()
    print(results)
