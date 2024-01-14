from sotanaut.llm_handling.config.llm_settings import (
    GPT3_TURBO_1106_OPEN_AI_Config,
    GPT4_1106_OPEN_AI_Config,
)
from sotanaut.llm_handling.models.model_factory import ModelFactory
from sotanaut.llm_handling.models.open_ai_api_model import OpenAIModel


def get_model():
    model_settings = GPT3_TURBO_1106_OPEN_AI_Config().get_params()
    model_type = model_settings["model_type"]
    return ModelFactory.get_model(model_type, model_settings)
