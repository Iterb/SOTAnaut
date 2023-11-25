class InferenceRunner:
    def build_prompt(self, template, system_message, prompt):
        """Construct the prompt using the template and provided keys/inputs."""
        return template.format(system_message=system_message, prompt=prompt)

    def run_inference(self, model_wrapper, full_prompt):
        return model_wrapper(full_prompt)
