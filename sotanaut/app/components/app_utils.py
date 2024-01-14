# app_utils.py
import streamlit as st
from langchain_openai import ChatOpenAI

from sotanaut.app.components.llm_loader import get_model
from sotanaut.app.components.llm_paper_retriever import LLMPaperRetriver
from sotanaut.llm_handling.agents.paper_agent import PaperAgent


def get_research_keywords(topic, use_llm):
    model = get_model()
    paper_retriever = LLMPaperRetriver(model)
    return paper_retriever.get_keywords(topic) if use_llm else get_default_keywords()


def get_default_keywords():
    return [
        "Cattle Parturition Prediction",
        "Bovine Birth Timing",
        "Cow Labor Contraction Monitoring",
        "Machine Learning in Livestock Birth Predictions",
        "Predictive Analytics for Animal Birthing",
    ]


def search_and_retrieve_papers(keywords, topic, use_llm):
    model = get_model()
    paper_retriever = LLMPaperRetriver(model)
    return paper_retriever.search_papers(keywords, topic, filter_and_rank_papers=use_llm)


def display_papers(papers):
    for paper in papers:
        with st.expander(paper.title):
            st.write("Authors:", paper.authors)
            st.write("Published:", paper.published)
            st.write("Summary:", paper.summary)
            st.write("Link:", paper.link)
            if st.button("Download Paper", key=paper.title):
                handle_paper_download(paper)


def handle_paper_download(paper):
    # Add logic to download the paper
    # e.g., paper.download_paper()
    st.write("Paper downloaded!")


def generate_insights(research_topic):
    # gpt-3.5-turbo
    llm = ChatOpenAI(model="gpt-4-1106-preview", temperature=0)
    paper_agent = PaperAgent(llm)
    return paper_agent.get_papers_summary(research_topic)
