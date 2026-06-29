import requests
import json
import os
import pandas as pd
from typing import Dict, Any, List
from dotenv import load_dotenv
from analytics.analytics_manager import AnalyticsManager
from cluster_descriptor_agent.agent import ClusterDescriptorAgent
from core.abstractions.strategy_descriptor import BaseStrategyDescriptor

class StrategyAnalyzerAgent(BaseStrategyDescriptor):
    def __init__(self, 
                 model_name: str = "gpt-oss:120b", 
                 prompt_file: str = "strategy_descriptor_agent/prompt.txt",
                 analytics_config: str = "analytics/analytics_config.yaml"):
        """
        Initializes the Strategy Analyzer Agent.
        Loads environment variables and sets up the internal analytics and description tools.
        """
        load_dotenv()
        self.model_name = model_name
        self.base_url = os.getenv("OLLAMA_CLOUD_URL", "https://ollama.com")
        self.api_key = os.getenv("OLLAMA_API_KEY", "")
        
        if not os.path.isabs(prompt_file):
            project_root = os.getcwd()
            prompt_path = os.path.join(project_root, prompt_file)
        else:
            prompt_path = prompt_file

        with open(prompt_path, 'r', encoding='utf-8') as f:
            self.prompt_template = f.read()
            
        self.analytics_manager = AnalyticsManager(analytics_config)
        self.descriptor_agent = ClusterDescriptorAgent(model_name=model_name)

    def analyze_strategy(self, competitor_products_path: str = "data/products_other_company.csv") -> str:
        try:
            our_clusters_raw = self.analytics_manager.get_clusters()
            our_clusters_desc = self.descriptor_agent.describe_all_clusters(our_clusters_raw)
            
            comp_clusters_raw = self.analytics_manager.get_clusters(products_path=competitor_products_path)
            comp_clusters_desc = self.descriptor_agent.describe_all_clusters(comp_clusters_raw)
            
            sales_stats = self.analytics_manager.run_analytics()
            
            our_clusters_str = "\n".join([f"- Cluster {cid}: {desc}" for cid, desc in our_clusters_desc.items()])
            comp_clusters_str = "\n".join([f"- Cluster {cid}: {desc}" for cid, desc in comp_clusters_desc.items()])
            sales_stats_str = sales_stats.to_string()
            
            prompt = self.prompt_template.format(
                our_clusters=our_clusters_str,
                competitor_clusters=comp_clusters_str,
                sales_analytics=sales_stats_str
            )
            
            url = f"{self.base_url.rstrip('/')}/api/generate"
            headers = {"Content-Type": "application/json"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            }

            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            
            return result.get("response", "No strategy analysis generated.")
            
        except Exception as e:
            return f"Error during strategy analysis: {str(e)}"

if __name__ == "__main__":
    print("Initializing Strategy Analyzer...")
    analyzer = StrategyAnalyzerAgent()
    
    print("Running full strategic analysis (this involves multiple AI calls)...")
    report = analyzer.analyze_strategy(competitor_products_path="data/products_other_company.csv")
    
    print("\n" + "="*50)
    print("STRATEGIC ANALYSIS REPORT")
    print("="*50)
    print(report)
    print("="*50)
