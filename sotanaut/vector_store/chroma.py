"""Inspired by https://github.com/snexus/llm-search"""

import logging
import shutil
from pathlib import Path
from typing import List, Tuple

from langchain.vectorstores import Chroma

from sotanaut.vector_store.base import VectorStore
from sotanaut.vector_store.embeddings import EmbeddingsType, get_embedding_model


class VectorStoreChroma(VectorStore):
    def __init__(self, persist_folder: str, embeddings_type: EmbeddingsType):
        self._persist_folder = persist_folder
        self._embeddings = get_embedding_model(embeddings_type)
        self._retriever = None

    @property
    def retriever(self):
        if self._retriever is None:
            self._retriever = self._load_retriever()
        return self._retriever

    def create_index_from_documents(
        self,
        all_docs,
        clear_persist_folder: bool = True,
    ):
        if clear_persist_folder:
            pf = Path(self._persist_folder)
            if pf.is_dir():
                logging.warning(f"Deleting the content of: {pf}")
                shutil.rmtree(pf)

        logging.info("Generating and persisting the embeddings..")
        ids = [doc.metadata["document_id"] for doc in all_docs]
        vectordb = Chroma.from_documents(
            documents=all_docs,
            embedding=self._embeddings,
            ids=ids,
            persist_directory=self._persist_folder,  # type: ignore
        )
        vectordb.persist()

    def _load_retriever(self, **kwargs):
        vectordb = Chroma(
            persist_directory=self._persist_folder, embedding_function=self._embeddings
        )
        return vectordb.as_retriever(**kwargs)

    def get_documents_by_id(self, document_ids: List[str]):
        """Retrieves documents by ids.

        Args:
            document_ids (List[str]): list of document ids

        Returns:
            List[Document]: list of documents belonging to document_ids
        """

        results = self.retriever.vectorstore.get(ids=document_ids, include=["metadatas", "documents"])  # type: ignore
        docs = [
            Document(page_content=d, metadata=m)
            for d, m in zip(results["documents"], results["metadatas"])
        ]
        return docs

    def similarity_search_with_relevance_scores(
        self, query: str, k: int, filter: dict
    ) -> List[Tuple[Document, float]]:
        return self.retriever.vectorstore.similarity_search_with_relevance_scores(
            query, k=self._config.semantic_search.max_k, filter=filter
        )  # type: ignore
