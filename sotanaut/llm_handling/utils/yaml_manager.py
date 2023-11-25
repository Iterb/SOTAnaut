from enum import Enum
from pathlib import Path

import yaml


class YAMLCategory(Enum):
    PROMPT = "prompts"
    SYSTEM_MESSAGE = "system_messages"
    TEMPLATE = "templates"
    UTLS = "utils"


class YAMLFileNotFoundError(Exception):
    pass


class YAMLKeyNotFoundError(Exception):
    pass


class YAMLManager:
    YAML_DIR = Path(__file__).parent.parent / "yamls"

    def __init__(self):
        self.data = {category: {} for category in YAMLCategory}

    def _load_yaml(self, category, key):
        yaml_path = self.YAML_DIR / category.value / f"{key}.yaml"
        if not yaml_path.exists() or yaml_path.suffix != ".yaml":
            raise YAMLFileNotFoundError(
                f"YAML file for '{key}' in category '{category.value}' not found."
            )

        with yaml_path.open("r") as f:
            self.data[category][key] = yaml.safe_load(f)

    def get(self, category, key):
        if key not in self.data[category]:
            self._load_yaml(category, key)

        try:
            return self.data[category][key]
        except KeyError:
            available_keys = list(self.data[category].keys())
            raise YAMLKeyNotFoundError(
                f"'{key}' not found in category '{category.value}'. Available keys: {available_keys}"
            )

    @staticmethod
    def merge_prompts(*prompts: str, separator="\n"):
        valid_prompts = [prompt for prompt in prompts if prompt]
        return separator.join(valid_prompts)
