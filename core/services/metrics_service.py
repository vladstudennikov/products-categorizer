class MetricsService:
    def calculate_cluster_count(self, labels):
        return len(
            {
                label
                for label in labels
                if label != -1
            }
        )
