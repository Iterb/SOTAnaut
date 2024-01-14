from elasticsearch_dsl import Search
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.docstore.document import Document
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain.tools.retriever import create_retriever_tool
from langchain_community.vectorstores import FAISS
from langchain_core.messages import SystemMessage

from sotanaut.db_handling.es_connection import create_connection, get_connection
from sotanaut.llm_handling.parsing.prompt_builder import PromptBuilder, PromptType


class PaperAgent:
    PAPER_TOOL_TEMPLATE = "Search the paper titled {title}. For any questions about found papers, you must use this tool!"

    def __init__(self, model):
        self.db_client = self._connect_to_db()
        self.paper_tools = self._build_paper_tools()
        self.prompt_builder = PromptBuilder()

        self.model = model
        self.engine = None

    def _read_all_papers_from_db(self):  #! REBUILD THE DATABASES TO BE MORE SEPARATED
        INDEX = "research-papers"  # ? move somewhere global
        search = Search(using=self.db_client, index=INDEX).source(includes=[])
        return search.execute()

    def _read_db_paper_to_documents(self, paper):
        text_splitter = CharacterTextSplitter()
        texts = text_splitter.split_text(paper.full_text)
        documents = [Document(page_content=t) for t in texts]
        return RecursiveCharacterTextSplitter(
            separators=[". ", "\n"], chunk_size=1000, chunk_overlap=200
        ).split_documents(documents)

    def _build_paper_tools(self):
        db_papers = self._read_all_papers_from_db()
        paper_tools = []
        for db_paper_number, db_paper in enumerate(db_papers):
            paper_documents = self._read_db_paper_to_documents(db_paper)
            vector = FAISS.from_documents(paper_documents, OpenAIEmbeddings())
            retriever = vector.as_retriever()
            paper_tools.append(
                create_retriever_tool(
                    retriever,
                    f"Academic_paper_{db_paper_number}",
                    self.PAPER_TOOL_TEMPLATE.format(title=db_paper.title),
                )
            )
        return paper_tools

    def _build_engine(self, prompt):
        agent = create_openai_functions_agent(self.model, self.paper_tools, prompt)
        return AgentExecutor(agent=agent, tools=self.paper_tools, verbose=True)

    def _build_prompt(self, system_message, human_message):
        return ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(system_message),
                MessagesPlaceholder(variable_name="chat_history", optional=True),
                HumanMessagePromptTemplate.from_template(human_message),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

    def _connect_to_db(self):
        create_connection()
        return get_connection()

    def get_papers_summary(self, research_topic):
        system_message = self.prompt_builder.get_system_message(
            prompt_type=PromptType.PAPER_SUMMARIZATION
        )
        human_message = self.prompt_builder.get_user_prompt(
            prompt_type=PromptType.PAPER_SUMMARIZATION,
            research_topic=research_topic,
        )
        prompt = self._build_prompt(system_message, human_message)
        engine = self._build_engine(prompt)
        return engine.invoke({"research_topic": research_topic})

    def get_methods_summary():
        """Most important things out of papers."""

    def get_dataset_summary():
        """Most important things out of papers."""
