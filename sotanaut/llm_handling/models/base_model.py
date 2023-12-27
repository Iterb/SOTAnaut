from __future__ import annotations

from abc import ABC, abstractmethod


class BaseModel(ABC):
    @abstractmethod
    def run_inference(self, system_message, prompt):
        pass

    @classmethod
    @abstractmethod
    def load_model(cls, config):
        pass
