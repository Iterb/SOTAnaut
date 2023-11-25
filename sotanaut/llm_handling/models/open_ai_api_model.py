import logging
from openai import OpenAI
import os
import json

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s",
    level=logging.INFO,
)

class OpenAIModel:

    def __init__(self, client, input_template, model_id):
        self._client = client
        self._input_template = input_template
        self._model_id = model_id

        
    @classmethod
    def load_model(cls, model_id, input_template, **kwargs):
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Provide the OPENAI_API_KEY in env var to use OPEN AI model")
        
        client = OpenAI(
          api_key=api_key
        )

        return cls(client, input_template, model_id)
    
    def run_inference(self, system_message, prompt):
        full_prompt = self._input_template.format(system_message=system_message, prompt=prompt)
        full_prompt = full_prompt.replace("\n", " ")
        messages = json.loads(full_prompt)
        completion = self._client.chat.completions.create(
            model=self._model_id,
            messages=messages
        )
        return completion.choices[0].message.content