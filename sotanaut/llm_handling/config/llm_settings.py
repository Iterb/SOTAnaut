from __future__ import annotations

from typing import NamedTuple

from sotanaut.llm_handling.models.base_model import BaseModel

# from sotanaut.llm_handling.models.local_model_transformers import LocalTransformerModel
from sotanaut.llm_handling.models.open_ai_api_model import OpenAIModel
from sotanaut.llm_handling.templates.template_bank import TemplateCategory, get_prompt

# class SDL_LLAMA_2_13B_Config(NamedTuple):

#     model_id = "TheBloke/sheep-duck-llama-2-13B-GPTQ"
#     model_type = LocalTransformerModel
#     model_basename = "model"
#     device_type = "cuda"
#     input_template = get_prompt(TemplateCategory.TEMPLATE, "basic_templates")["orca_hashes"]


class GPT4_1106_OPEN_AI_Config(NamedTuple):
    model_id = "gpt-4-1106-preview"
    model_type = OpenAIModel
    input_template = get_prompt(TemplateCategory.TEMPLATE, "basic_templates")["open_ai"]


class GPT3_TURBO_1106_OPEN_AI_Config(NamedTuple):
    model_id: str = "gpt-3.5-turbo-1106"
    model_type: BaseModel = OpenAIModel
    input_template: str = get_prompt(TemplateCategory.TEMPLATE, "basic_templates")["open_ai"]


class GPT3_TURBO_16K_OPEN_AI_Config(NamedTuple):
    model_id: str = "gpt-3.5-turbo-16k"
    model_type: BaseModel = OpenAIModel
    input_template: str = get_prompt(TemplateCategory.TEMPLATE, "basic_templates")["open_ai"]


MODELS = {
    # "LLAMA_2_13B": SDL_LLAMA_2_13B_Config(),
    "GPT4_1106": GPT4_1106_OPEN_AI_Config(),
    "GPT3_TURBO_1106": GPT3_TURBO_1106_OPEN_AI_Config(),
    "GPT3_TURBO_16k": GPT3_TURBO_16K_OPEN_AI_Config(),
}
