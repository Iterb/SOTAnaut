from sotanaut.llm_handling.config.llm_settings import (
    GPT3_TURBO_1106_OPEN_AI_Config,
    GPT4_1106_OPEN_AI_Config,
)
from sotanaut.llm_handling.models.model_factory import ModelFactory

# from sotanaut.llm_handling.models.local_model_transformers import LocalTransformersModel
from sotanaut.llm_handling.models.open_ai_api_model import OpenAIModel
from sotanaut.llm_handling.parsing.prompt_builder import PromptBuilder
from sotanaut.paper_retrieval.sources.arxiv import ArxivSource
from sotanaut.paper_retrieval.sources.google_scholar import GoogleScholarSource
from sotanaut.paper_retrieval.sources.pubmed import PubmedSource

if __name__ == "__main__":
    model_settings = GPT4_1106_OPEN_AI_Config().get_params()
    model_type = model_settings["model_type"]
    model = ModelFactory.get_model(model_type, model_settings)

    sources = [ArxivSource(), PubmedSource(), GoogleScholarSource()]
    prompt_builder = PromptBuilder()
    research_topic = "Trying to predict the cows birth time based on the body contractions"

    system_message = prompt_builder.get_system_message(prompt_type="keyword_generation")
    user_prompt = prompt_builder.get_user_prompt(
        prompt_type="keyword_generation",
        output_formats={"enumerated_list": None, "limit_output": {"limit_value": 5}},
        research_topic=research_topic,
    )

    response = model.run_inference(system_message, user_prompt)
    print(response)

    # keywords = LLMParser.parse_enumerated_output(response)
    # print(keywords)
    # keywords = ["Flower Image Classification","Plant Identification","Botanical Recognition","Floral Category Detection","Computer Vision in Botany","Machine Learning for Flowers","Deep Learning for Plants","CNN for Plant Identification","SVM for Floral Categories","RGB Analysis for Flowers","Color Spectrum Extraction for Plants","Feature Selection for Flower Images","Data Augmentation for Botanical Datasets","Transfer Learning for Plant Identification","Ensemble Methods for Flower Classification","Performance Evaluation in Flower Recognition","Benchmark Datasets for Plant Identification","Challenges in Flower Image Classification","Future Directions in Floral Recognition Research"]
    # # keywords = ["precision agriculture", "crop yield prediction", "disease detection in plants", "soil nutrient analysis using ML"]
    # # keywords = ["fraud detection using deep learning", "stock market prediction algorithms", "customer spending pattern analysis", "credit scoring with ML"]
    keywords = [
        "Cow parturition prediction",
        "Bovine birth timing contractions",
        "Predictive models for calving",
        "Labor contraction monitoring in cows",
        "Machine learning in cow birth prediction",
        # "AI/ML solutions",
        # "Pre-calving behavior patterns",
        # "Automated calving detection systems",
        # "Cattle parturition signs",
        # "Real-time monitoring of bovine labor",
        # "Precision livestock farming calving",
    ]
    papers = []
    for source in sources:
        papers.extend(source.get_papers(keywords, max_results=5))
    paper_descriptions = [
        f"{(paper_num+1)}. {paper.short_description()}" for paper_num, paper in enumerate(papers)
    ]

    system_message = prompt_builder.get_system_message(prompt_type="paper_filtering")
    user_prompt = prompt_builder.get_user_prompt(
        prompt_type="paper_filtering",
        output_formats={"enumerated_list": None, "limit_output": {"limit_value": 5}},
        research_topic=research_topic,
        papers=paper_descriptions,
    )

    print(system_message)
    print(user_prompt)

    response = model.run_inference(system_message, user_prompt)

    print(response)
