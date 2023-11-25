from sotanaut.llm_handling.config.llm_settings import SDL_LLAMA_2_13B, GPT4_1106_OPEN_AI
# from sotanaut.llm_handling.models.local_model_transformers import LocalTransformersModel
from sotanaut.llm_handling.models.open_ai_api_model import OpenAIModel
from sotanaut.llm_handling.utils.llm_parser import LLMParser
from sotanaut.llm_handling.utils.yaml_manager import YAMLManager, YAMLCategory
from sotanaut.paper_retrieval.sources.arxiv import ArxivSource


if __name__ == "__main__":
    yaml_manager = YAMLManager()
    model_settings = GPT4_1106_OPEN_AI #SDL_LLAMA_2_13B
    
    template = yaml_manager.get(YAMLCategory.TEMPLATE, "basic_templates")[model_settings.pop("input_template")]
    
    model = OpenAIModel.load_model(**model_settings, input_template=template)
    arxiv_source = ArxivSource()
    
    research_topic = "Flower Image Classification"
    prompt = yaml_manager.get(YAMLCategory.PROMPT, "keyword_generation")["default"]
    prompt = prompt.format(user_input_topic=research_topic)
    
    format_prompt = yaml_manager.get(YAMLCategory.UTLS, "output_format")["enumerated_list"]
    output_limit_prompt = yaml_manager.get(YAMLCategory.UTLS, "output_format")["limit_output"]
    output_limit_prompt = output_limit_prompt.format(limit_value=10)
    full_user_prompt = LLMParser.merge_prompts(prompt, format_prompt, output_limit_prompt, separator="")
    system_message = yaml_manager.get(YAMLCategory.SYSTEM_MESSAGE, "keyword_generation")["default"]
    
    response = model.run_inference(system_message, full_user_prompt)
    print(response)
    
    keywords = LLMParser.parse_enumerated_output(response)
    print(keywords)
    # keywords = ["Flower Image Classification","Plant Identification","Botanical Recognition","Floral Category Detection","Computer Vision in Botany","Machine Learning for Flowers","Deep Learning for Plants","CNN for Plant Identification","SVM for Floral Categories","RGB Analysis for Flowers","Color Spectrum Extraction for Plants","Feature Selection for Flower Images","Data Augmentation for Botanical Datasets","Transfer Learning for Plant Identification","Ensemble Methods for Flower Classification","Performance Evaluation in Flower Recognition","Benchmark Datasets for Plant Identification","Challenges in Flower Image Classification","Future Directions in Floral Recognition Research"]
    # # keywords = ["precision agriculture", "crop yield prediction", "disease detection in plants", "soil nutrient analysis using ML"]
    # # keywords = ["fraud detection using deep learning", "stock market prediction algorithms", "customer spending pattern analysis", "credit scoring with ML"]
    papers = arxiv_source.get_papers(keywords)
    print(papers[0])