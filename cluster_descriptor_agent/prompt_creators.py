from typing import List

class BasePromptCreator:
    def create_prompt(*args):
        raise NotImplementedError("BasePromptCreator could not be used to create prompt")
    
class ClusterFilePromptCreator(BasePromptCreator):
    def __init__(self, prompt_file: str = "cluster_descriptor_agent/prompt.txt"):
        with open(prompt_file, 'r') as f:
            self.prompt_template = f.read()
        
        
    def create_prompt(self, product_names: List[str]) -> str:
        return self.prompt_template.format(product_names=", ".join(product_names))