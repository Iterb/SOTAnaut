from typing import List, Literal, Optional

from sotanaut.llm_handling.yamls.yaml_manager import YAMLCategory, YAMLManager


class PromptBuilder:
    def __init__(self):
        self.yaml_manager = YAMLManager()

    @staticmethod
    def merge_prompts(*prompts: str, separator="\n") -> str:
        """Merges multiple prompt strings into one.

        Args:
            *prompts: Variable length prompt list.
            separator (str): The separator to use between prompts.

        Returns:
            str: A single merged prompt string.
        """
        valid_prompts = [prompt for prompt in prompts if prompt]
        return separator.join(valid_prompts)

    def get_system_message(
        self,
        prompt_type: Literal["keyword_generation", "paper_filtering"],  # TODO make enum
        prompt_variation: str = "default",  # TODO also formalize
    ):
        return self.yaml_manager.get(YAMLCategory.SYSTEM_MESSAGE, prompt_type)[prompt_variation]

    def get_user_prompt(
        self,
        prompt_type: Literal["keyword_generation", "paper_filtering"],  # TODO make enum
        prompt_variation: str = "default",  # TODO also formalize
        output_formats: Optional[dict] = None,
        **kwargs,
    ):
        prompt = self.yaml_manager.get(YAMLCategory.PROMPT, prompt_type)[prompt_variation]
        prompt = prompt.format(**kwargs)
        output_format_prompts = []
        if output_formats:
            for output_format, additional_kwargs in output_formats.items():
                util_prompt = self.yaml_manager.get(YAMLCategory.UTLS, "output_format")[
                    output_format
                ]
                if additional_kwargs:
                    util_prompt = util_prompt.format(**additional_kwargs)
                output_format_prompts.append(util_prompt)
        return PromptBuilder.merge_prompts(prompt, *output_format_prompts, separator="")
