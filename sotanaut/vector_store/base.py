"""Inspired by https://github.com/snexus/llm-search"""

from abc import ABC, abstractmethod
from typing import List


class VectorStore(ABC):
    @abstractmethod
    def create_index_from_documents(self, all_docs, clear_persist_folder: bool = True):
        pass

    @abstractmethod
    def get_documents_by_id(self, docuemt_ids: List[str]):
        pass

    @property
    @abstractmethod
    def retriever(self):
        pass

    @abstractmethod
    def similarity_search_with_relevance_scores(self, query: str, k: int, filter: dict):
        pass
