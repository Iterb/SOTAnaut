from sotanaut.llm_handling.config.llm_settings import SDL_LLAMA_2_13B
from sotanaut.llm_handling.models.llm_wrapper import ModelWrapper
from sotanaut.paper_retrieval.sources.arxiv import ArxivSource


if __name__ == "__main__":
    # model = ModelWrapper.load_model(**SDL_LLAMA_2_13B, device_type="cuda")
    arxiv_source = ArxivSource()
    
    keywords = ["precision agriculture", "crop yield prediction", "disease detection in plants", "soil nutrient analysis using ML"]
    keywords = ["fraud detection using deep learning", "stock market prediction algorithms", "customer spending pattern analysis", "credit scoring with ML"]
    papers = arxiv_source.get_papers(keywords)
    print(papers[0])