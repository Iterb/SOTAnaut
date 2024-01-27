from __future__ import annotations

import logging
import os

from openai import OpenAI

from sotanaut.llm_handling.models.base_model import BaseModel
from sotanaut.llm_handling.utils.general_utils import validate_and_fix_json
from sotanaut.paper_retrieval.utils.helpers import fix_json_via_get

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s",
    level=logging.INFO,
)


class OpenAIModel(BaseModel):
    def __init__(self, client, input_template, model_id):
        self._client = client
        self._input_template = input_template
        self._model_id = model_id

    @classmethod
    def load_model(cls, model_id, input_template, **kwargs):
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Provide the OPENAI_API_KEY in env var to use OPEN AI model")

        client = OpenAI(api_key=api_key)

        return cls(client, input_template, model_id)

    def run_inference(self, system_message, prompt):
        # full_prompt = self._input_template.format(system_message=system_message, prompt=prompt) # hate this json parsing. I will disconnect it from interface and hardcode it for now.

        full_prompt = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt},
        ]
        # fixed_prompt = print(full_prompt)
        # full_prompt = full_prompt.replace("\n", " ")
        # fixed = validate_and_fix_json(full_prompt)
        # print(fixed)

        # problematic_part = full_prompt[max(0, 10-10):10+10]
        # good_json_string = repair_json(full_prompt)
        # print("HERHEHREHRHAHSDHASHD")
        # print(fix_json_via_get("{\"Much JSON!\":\"So Wow!\"}"))
        # messages = json.loads(good_json_string)
        completion = self._client.chat.completions.create(
            model=self._model_id, messages=full_prompt
        )
        return completion.choices[0].message.content
