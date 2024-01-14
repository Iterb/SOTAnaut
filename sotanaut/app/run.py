# main.py
import pyrootutils
import streamlit as st

root_path = pyrootutils.find_root(search_from=__file__, indicator=[".git", "setup.cfg"])
pyrootutils.set_root(
    path=root_path, project_root_env_var=True, dotenv=True, pythonpath=True, cwd=True
)

from sotanaut.app.components.app_utils import (
    display_papers,
    generate_insights,
    get_research_keywords,
    search_and_retrieve_papers,
)


def main():
    st.title("SOTAnaut")
    st.image("github_images/banner.png")

    research_topic = st.text_input("Enter a research topic:")
    search_button, use_llm = setup_ui()

    if search_button and research_topic:
        keywords = get_research_keywords(research_topic, use_llm)
        st.write("Keywords:", ", ".join(keywords))

        papers = search_and_retrieve_papers(keywords, research_topic, use_llm)
        display_papers(papers)

        if papers:
            generate_summary = st.button("Generate insights")

        if generate_summary:
            summary = generate_insights(research_topic)
            st.write(summary)


def setup_ui():
    col1, col2 = st.columns(2)
    with col1:
        search_button = st.button("Search")
    with col2:
        use_llm = st.checkbox("Activate model", value=False)
    return search_button, use_llm


if __name__ == "__main__":
    main()
