import logging

import torch
from auto_gptq import AutoGPTQForCausalLM
from langchain.llms import HuggingFacePipeline
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    GenerationConfig,
    LlamaForCausalLM,
    LlamaTokenizer,
    pipeline,
)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s",
    level=logging.INFO,
)


class ModelWrapper:

    def __init__(self, pipeline):
        self.pipeline = pipeline

    @classmethod
    def load_model(cls, model_id, device_type, model_basename=None):
        logging.info(f"Loading Model: {model_id}, on: {device_type}")
        logging.info("This action can take a few minutes!")

        tokenizer, model = cls._load_model_and_tokenizer(
            model_id, device_type, model_basename)
        pipeline = cls._create_text_generation_pipeline(model_id, tokenizer, model)
        return cls(pipeline)
    
    @staticmethod
    def _load_model_and_tokenizer(model_id, device_type, model_basename):
        if model_basename:
            return ModelWrapper._load_quantized_model_and_tokenizer(model_id, model_basename)
        elif device_type.lower() == 'cuda':
            return ModelWrapper._load_full_model_and_tokenizer(model_id)
        else:
            return ModelWrapper._load_llama_model_and_tokenizer(model_id)

    @staticmethod
    def _load_quantized_model_and_tokenizer(model_id, model_basename):
        logging.info("Using AutoGPTQForCausalLM for quantized models")

        if ".safetensors" in model_basename:
            model_basename = model_basename.replace(".safetensors", "")

        tokenizer = AutoTokenizer.from_pretrained(model_id)
        logging.info("Tokenizer loaded")

        model = AutoGPTQForCausalLM.from_quantized(
            model_id,
            model_basename=model_basename,
            use_safetensors=True,
            trust_remote_code=True,
            device="cuda:0",
            use_triton=False,
            quantize_config=None,
        )
        return tokenizer, model

    @staticmethod
    def _load_full_model_and_tokenizer(model_id):
        logging.info("Using AutoModelForCausalLM for full models")
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        logging.info("Tokenizer loaded")

        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            device_map="auto",
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
            trust_remote_code=True,
            # max_memory={0: "15GB"}  # Uncomment this line with you encounter CUDA out of memory errors
        )
        model.tie_weights()
        return tokenizer, model

    @staticmethod
    def _load_llama_model_and_tokenizer(model_id):
        logging.info("Using LlamaTokenizer")
        tokenizer = LlamaTokenizer.from_pretrained(model_id)
        model = LlamaForCausalLM.from_pretrained(model_id)
        return tokenizer, model

    @staticmethod
    def _create_text_generation_pipeline(model_id, tokenizer, model):
        generation_config = GenerationConfig.from_pretrained(model_id)
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_length=2048,
            temperature=0,
            top_p=0.95,
            repetition_penalty=1.15,
            generation_config=generation_config,
        )

        local_llm = HuggingFacePipeline(pipeline=pipe)
        logging.info("Local LLM Loaded")

        return local_llm
    
    def run_inference(self, full_prompt):
        return self.pipeline(full_prompt)