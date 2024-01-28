from sotanaut.llm_handling.parsing.llm_parser import LLMParser
from sotanaut.llm_handling.parsing.prompt_builder import PromptBuilder, PromptType
from sotanaut.paper_retrieval.sources.arxiv import ArxivSource
from sotanaut.paper_retrieval.sources.google_scholar import GoogleScholarSource
from sotanaut.paper_retrieval.sources.pubmed import PubmedSource
from sotanaut.paper_retrieval.utils.helpers import find_best_match


class LLMPaperRetriver:
    def __init__(self, model):
        self.sources = [
            ArxivSource(),
            PubmedSource(),
            GoogleScholarSource(),
        ]  # Hardcode for now

        self.prompt_builder = PromptBuilder()
        self.model = model

    def get_keywords(self, research_topic):
        system_message = self.prompt_builder.get_system_message(
            prompt_type=PromptType.KEYWORD_GENERATION
        )
        user_prompt = self.prompt_builder.get_user_prompt(
            prompt_type=PromptType.KEYWORD_GENERATION,
            output_formats={"enumerated_list": None, "limit_output": {"limit_value": 5}},
            research_topic=research_topic,
        )

        response = self.model.run_inference(system_message, user_prompt)
        return LLMParser.parse_enumerated_output(response)

    def search_for_papers(self, keywords, research_topic, filter_and_rank_papers=True):
        papers = []
        for source in self.sources:
            papers.extend(source.get_papers(keywords, max_results=5))

        # paper_descriptions = [
        #     f"{(paper_num+1)}. {paper.short_description()}"
        #     for paper_num, paper in enumerate(papers)
        # ]
        paper_titles = [
            f"{(paper_num+1)}. {paper.title}" for paper_num, paper in enumerate(papers)
        ]
        if filter_and_rank_papers:
            system_message = self.prompt_builder.get_system_message(
                prompt_type=PromptType.PAPER_FILTERING
            )
            user_prompt = self.prompt_builder.get_user_prompt(
                prompt_type=PromptType.PAPER_FILTERING,
                output_formats={"enumerated_list": None, "concise": None},
                research_topic=research_topic,
                papers=paper_titles,
            )

            response = self.model.run_inference(system_message, user_prompt)
            filtered_paper_titles = LLMParser.parse_enumerated_output(response)
            return [
                find_best_match(llm_output_title, papers)
                for llm_output_title in filtered_paper_titles
            ]
        return papers
