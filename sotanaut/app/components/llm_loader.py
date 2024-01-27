from sotanaut.llm_handling.config.llm_settings import MODELS


def get_model(model_name):
    model_settings = MODELS[model_name]  #! add exist check
    model_type = model_settings.model_type
    print(model_settings._asdict())
    return model_type.load_model(**model_settings._asdict())
