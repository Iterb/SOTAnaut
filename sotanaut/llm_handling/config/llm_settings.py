from abc import ABC, abstractmethod

from sotanaut.llm_handling.utils.yaml_manager import YAMLCategory, YAMLManager

class BaseModelConfig(ABC):

    @property
    @abstractmethod
    def model_id(self):
        """Abstract property for model_id."""
        pass
    
    @property
    @abstractmethod
    def model_type(self):
        """Abstract property for model_id."""
        pass

    @property
    @abstractmethod
    def input_template(self):
        """Abstract property for input_template."""
        pass

    @abstractmethod
    def get_params(self):
        """Abstract method to get model loading parameters."""
        pass
    
    def get_template(self):
        yaml_manager = YAMLManager()
        template = yaml_manager.get(YAMLCategory.TEMPLATE, "basic_templates")[self.input_template]
        return template
        
    
class SDL_LLAMA_2_13B_Config(BaseModelConfig):

    @property
    def model_id(self):
        return "TheBloke/sheep-duck-llama-2-13B-GPTQ"

    @property
    def model_type(self):
        return "OPEN_AI"
    
    @property
    def input_template(self):
        return "orca_hashes"
    
    def get_params(self):
        return {
            "model_id": self.model_id,
            "model_basename": "model",
            "model_type": self.model_type,
            "input_template": self.get_template(),
            "device_type": "cuda",
        }

class GPT4_1106_OPEN_AI_Config(BaseModelConfig):

    @property
    def model_id(self):
        return "gpt-4-1106-preview"

    @property
    def input_template(self):
        return "open_ai"
    
    @property
    def model_type(self):
        return "LOCAL_TRANSFORMER"

    def get_params(self):
        return {
            "model_id": self.model_id,
            "input_template": self.get_template(),
            "model_type": self.model_type,
        }