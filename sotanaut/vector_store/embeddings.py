import logging
from enum import Enum

from langchain.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings


class EmbeddingsType(Enum):
    huggingface = "huggingface"
    open_ai = "open_ai"


EMBEDDINGS = {
    EmbeddingsType.huggingface: HuggingFaceEmbeddings,
    EmbeddingsType.open_ai: OpenAIEmbeddings,
}


def get_embedding_model(embeddings_type: EmbeddingsType):
    """Loads an embedidng model.

    Args:
        config (EmbeddingModel): Configuration for the embedding model

    Raises:
        TypeError: if model is unsupported
    """

    logging.info(f"Embedding model type: {embeddings_type.value}")
    embeddings = EMBEDDINGS.get(embeddings_type.type)

    if embeddings is None:
        raise TypeError(f"Unknown embeddings type. Got {embeddings_type.value}")

    return embeddings()
