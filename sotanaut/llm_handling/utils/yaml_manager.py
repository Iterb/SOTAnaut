import yaml
from pathlib import Path
from enum import Enum

class YAMLCategory(Enum):
    PROMPT = "prompts"
    SYSTEM_MESSAGE = "system_messages"
    TEMPLATE = "templates"

class YAMLManager:
    
    YAML_DIR = Path(__file__).parent.parent / 'yamls'
    
    def __init__(self):
        self.data = {
            YAMLCategory.PROMPT: {},
            YAMLCategory.SYSTEM_MESSAGE: {},
            YAMLCategory.TEMPLATE: {}
        }
        self._load_all_yamls()

    def _load_all_yamls(self):
        for category in YAMLCategory:
            category_dir = self.YAML_DIR / category.value
            for yaml_file in category_dir.iterdir():
                if yaml_file.suffix == '.yaml':
                    with yaml_file.open('r') as f:
                        self.data[category][yaml_file.stem] = yaml.safe_load(f)

    def get(self, category, key):
        try:
            return self.data[category][key]
        except KeyError:
            available_keys = list(self.data[category].keys())
            print(f"'{key}' not found in category '{category.value}'. Available keys: {available_keys}")
            return None
