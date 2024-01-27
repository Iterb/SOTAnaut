# main.py or a separate logging_config.py
import logging

from elasticsearch_dsl import connections

from sotanaut.app.components.app_utils import generate_insights
from sotanaut.app.components.llm_loader import get_model
from sotanaut.app.components.llm_paper_retriever import LLMPaperRetriver
from sotanaut.db_handling.es_connection import create_connection
from sotanaut.db_handling.es_indexer import (
    ResearchPaper,
    ensure_elasticsearch_initialized,
    index_paper_to_elasticsearch,
)
from sotanaut.llm_handling.config.llm_settings import (
    GPT3_TURBO_1106_OPEN_AI_Config,
    GPT4_1106_OPEN_AI_Config,
)

# from sotanaut.llm_handling.models.local_model_transformers import LocalTransformersModel
from sotanaut.llm_handling.parsing.prompt_builder import PromptBuilder, PromptType
from sotanaut.paper_retrieval.downloader import PaperDownloader
from sotanaut.paper_retrieval.sources.arxiv import ArxivSource
from sotanaut.paper_retrieval.sources.google_scholar import GoogleScholarSource
from sotanaut.paper_retrieval.sources.pubmed import PubmedSource
from sotanaut.paper_retrieval.utils.helpers import find_best_match

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == "__main__":
    create_connection()
    ensure_elasticsearch_initialized()

    model = get_model("GPT3_TURBO_1106")
    paper_retriever = LLMPaperRetriver(model)

    sources = [
        ArxivSource(),
        PubmedSource(),
        GoogleScholarSource(),
    ]
    research_topic = "Trying to predict the cows birth time based on the body contractions"

    keywords = paper_retriever.get_keywords(research_topic)
    print(keywords)
    # keywords = [
    #     "Cow parturition prediction",
    #     "Bovine birth timing contractions",
    #     "Predictive models for calving",
    #     "Labor contraction monitoring in cows",
    #     "Machine learning in cow birth prediction",
    #     # "AI/ML solutions",
    #     # "Pre-calving behavior patterns",
    #     # "Automated calving detection systems",
    #     # "Cattle parturition signs",
    #     # "Real-time monitoring of bovine labor",
    #     # "Precision livestock farming calving",
    # ]
    papers = paper_retriever.search_for_papers(keywords, research_topic)
    for paper in papers:
        print(paper.title)
    # summary = generate_insights(research_topic)
    # print(summary)

    # response = model.run_inference(system_message, user_prompt)
    # print(response)
    # filtered_paper_titles = LLMParser.parse_enumerated_output(response)
    # print(filtered_paper_titles)
    # choosen_papers = [find_best_match(llm_output_title ,papers) for llm_output_title in filtered_paper_titles]
    # paper_status = {}
    # for paper in papers: # choosen_papers:
    #     saved_to_db = False
    #     paper_downloader = PaperDownloader(paper)
    #     if file_path := paper_downloader.download_paper(
    #         folder_path="downloaded/"
    #     ):
    #         print(paper.id)
    #         saved_to_db = index_paper_to_elasticsearch(paper, file_path)
    #     paper_status[paper.title] = saved_to_db
    # print(paper_status)
