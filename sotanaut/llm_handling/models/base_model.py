from abc import ABC, abstractmethod

class BaseModel(ABC):

    @abstractmethod
    def run_inference(self, system_message, prompt):
        pass
    
    @abstractmethod
    @classmethod
    def load_model(cls, config):
        pass