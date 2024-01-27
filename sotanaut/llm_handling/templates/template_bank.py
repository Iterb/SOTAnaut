from enum import Enum
from pathlib import Path

import yaml


class TemplateCategory(Enum):  # ? Maybe it should be in prompt builder or handled
    PROMPT = "prompts"
    SYSTEM_MESSAGE = "system_messages"
    TEMPLATE = "templates"
    UTILS = "utils"


class YAMLFileNotFoundError(Exception):
    pass


class YAMLKeyNotFoundError(Exception):
    pass


class TemplateBank:
    YAML_DIR = Path(__file__).parent.parent / "templates"
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.data = {category: {} for category in TemplateCategory}

    def _load_yaml(self, category, key):
        yaml_path = self.YAML_DIR / category.value / f"{key}.yaml"
        if not yaml_path.exists() or yaml_path.suffix != ".yaml":
            raise YAMLFileNotFoundError(
                f"YAML file for '{key}' in category '{category.value}' not found."
            )

        with yaml_path.open("r") as f:
            self.data[category][key] = yaml.safe_load(f)

    def get(self, category, key):  # ? Keys could be PromptType enums
        if key not in self.data[category]:
            self._load_yaml(category, key)

        try:
            return self.data[category][key]
        except KeyError as e:
            available_keys = list(self.data[category].keys())
            raise YAMLKeyNotFoundError(
                f"'{key}' not found in category '{category.value}'. Available keys: {available_keys}"
            ) from e


def get_prompt(category, key):
    return TemplateBank.get_instance().get(category, key)
