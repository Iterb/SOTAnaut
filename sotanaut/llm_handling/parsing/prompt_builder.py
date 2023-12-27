from __future__ import annotations

from enum import Enum
from typing import Any

from sotanaut.llm_handling.yamls.yaml_manager import YAMLCategory, YAMLManager


class PromptType(Enum):
    """Enumeration for different types of prompts.

    Attributes:
        KEYWORD_GENERATION: Represents a prompt type for keyword generation.
        PAPER_FILTERING: Represents a prompt type for paper filtering.
    """

    KEYWORD_GENERATION = "keyword_generation"
    PAPER_FILTERING = "paper_filtering"


class PromptVariation(Enum):
    """Enumeration for different variations of prompts.

    Attributes:
        DEFAULT: Represents the default variation of a prompt.
    """

    DEFAULT = "default"


class PromptBuilder:
    """A builder class for constructing prompt strings from YAML configurations.

    Attributes:
        yaml_manager (YAMLManager): An instance of YAMLManager to manage YAML file operations.
    """

    def __init__(self):
        """Initializes the PromptBuilder with a YAMLManager instance."""
        self.yaml_manager = YAMLManager()

    @staticmethod
    def merge_prompts(*prompts: str, separator: str = "\n") -> str:
        """Merges multiple prompt strings into a single string.

        Args:
            *prompts: Variable number of string prompts to merge.
            separator: The separator to use between prompts.

        Returns:
            A single merged prompt string.
        """
        valid_prompts = [prompt for prompt in prompts if prompt]
        return separator.join(valid_prompts)

    def get_system_message(
        self, prompt_type: PromptType, prompt_variation: PromptVariation = PromptVariation.DEFAULT
    ) -> str:
        """Retrieves a system message based on the specified prompt type and variation.

        Args:
            prompt_type: The type of the prompt as defined in PromptType.
            prompt_variation: The variation of the prompt, default is 'default'.

        Returns:
            A string representing the system message.

        Raises:
            ValueError: If the YAML configuration is invalid or missing required keys.
        """
        try:
            return self.yaml_manager.get(YAMLCategory.SYSTEM_MESSAGE, prompt_type.value)[
                prompt_variation.value
            ]
        except KeyError as e:
            raise ValueError(f"Invalid configuration for system message: {e}") from e

    def get_user_prompt(
        self,
        prompt_type: PromptType,
        prompt_variation: PromptVariation = PromptVariation.DEFAULT,
        output_formats: dict[str, Any] | None = None,
        **kwargs,
    ) -> str:
        """Constructs a user prompt based on the specified type, variation, and output formats.

        Args:
            prompt_type: The type of the prompt as defined in PromptType.
            prompt_variation: The variation of the prompt, default is 'default'.
            output_formats: Optional dictionary specifying additional format configurations.
            **kwargs: Additional keyword arguments to be formatted within the prompt.

        Returns:
            A formatted user prompt string.

        Raises:
            ValueError: If the YAML configuration is invalid or missing required keys.
        """
        try:
            prompt = self.yaml_manager.get(YAMLCategory.PROMPT, prompt_type.value)[
                prompt_variation.value
            ].format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Invalid configuration for user prompt: {e}") from e

        output_format_prompts = []
        if output_formats:
            for output_format, additional_kwargs in output_formats.items():
                try:
                    util_prompt = self.yaml_manager.get(YAMLCategory.UTILS, "output_format")[
                        output_format
                    ].format(**additional_kwargs)
                    output_format_prompts.append(util_prompt)
                except KeyError as e:
                    raise ValueError(f"Invalid configuration for output format: {e}") from e

        return self.merge_prompts(
            prompt, *output_format_prompts, separator=""
        )  # ? Now without jsoning it I could change the separator to \n
