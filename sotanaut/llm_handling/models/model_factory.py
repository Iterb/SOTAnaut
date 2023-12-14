class ModelFactory:
    registry = {}

    @classmethod
    def register(cls, key):
        def inner_wrapper(wrapped_class):
            if key in cls.registry:
                raise ValueError(f"Key '{key}' already exists in Model Registry")
            cls.registry[key] = wrapped_class
            return wrapped_class

        return inner_wrapper

    @classmethod
    def get_model(cls, key, config):
        if key not in cls.registry:
            raise ValueError(f"Model '{key}' not found in registry")
        model_class = cls.registry[key]
        return model_class.load_model(**config)
