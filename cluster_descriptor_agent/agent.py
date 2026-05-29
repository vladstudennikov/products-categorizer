import requests
import json
import os
from typing import List
from dotenv import load_dotenv

class ClusterDescriptorAgent:
    def __init__(self, model_name: str = "gpt-oss:120b", prompt_file: str = "cluster_descriptor_agent/prompt.txt"):
        load_dotenv() # Load variables from .env file
        self.model_name = model_name
        self.base_url = os.getenv("OLLAMA_CLOUD_URL", "https://ollama.com") 
        self.api_key = os.getenv("OLLAMA_API_KEY", "")
        
        with open(prompt_file, 'r') as f:
            self.prompt_template = f.read()

    def describe_cluster(self, product_names: List[str]) -> str:
        prompt = self.prompt_template.format(product_names=", ".join(product_names))
        
        url = f"{self.base_url.rstrip('/')}/api/generate"
        
        headers = {
            "Content-Type": "application/json"
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "No description generated.")
        except Exception as e:
            return f"Error communicating with Ollama Cloud: {str(e)}"

    def describe_all_clusters(self, clusters_data: dict) -> dict:
        """
        Expects clusters_data to be a mapping of cluster_id to list of product names.
        """
        descriptions = {}
        for cluster_id, names in clusters_data.items():
            print(f"Describing cluster {cluster_id}...")
            descriptions[cluster_id] = self.describe_cluster(names)
        return descriptions
