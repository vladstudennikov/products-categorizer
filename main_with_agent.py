from analytics.analytics_manager import AnalyticsManager
from cluster_descriptor_agent.agent import ClusterDescriptorAgent
import pandas as pd

def main():
    # 1. Generate Clusters using the existing clusterizer
    print("Generating Clusters...")
    manager = AnalyticsManager("analytics/analytics_config.yaml")
    # This method uses the core clusterizer and returns {cluster_id: [product_names]}
    clusters_to_describe = manager.get_clusters()
    
    # 2. Pass these clusters DIRECTLY to the agent
    print("Starting Cluster Descriptor Agent (Ollama Cloud)...")
    agent = ClusterDescriptorAgent(model_name="gpt-oss:120b")
    descriptions = agent.describe_all_clusters(clusters_to_describe)

    # 3. Present Results
    print("\n--- Final AI-Generated Cluster Reports ---")
    for cluster_id, desc in descriptions.items():
        # -1 is the label for noise in DBSCAN
        label = "Noise/Unclustered" if cluster_id == "-1" else f"Cluster {cluster_id}"
        print(f"\n[{label}]")
        print(desc)

if __name__ == "__main__":
    main()
