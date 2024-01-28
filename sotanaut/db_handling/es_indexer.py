import logging

from elasticsearch.exceptions import NotFoundError
from elasticsearch_dsl import Date, Document, Search, Text
from PyPDF2.errors import PdfReadError

from sotanaut.db_handling.es_connection import ESConnection
from sotanaut.db_handling.utils import extract_text_from_pdf


class ResearchPaper(Document):
    id = Text()
    title = Text()
    authors = Text()
    publication_date = Date()
    source_url = Text()
    full_text = Text()

    class Index:
        name = "research-papers"

    @classmethod
    def ensure_index_initialized(cls):
        try:
            if not cls._index.exists():
                cls.init()
        except NotFoundError:
            cls.init()

    @classmethod
    def index_paper(cls, paper, file_path):
        try:
            full_text = extract_text_from_pdf(file_path)
            es_paper = cls(
                id=str(paper.id),
                title=paper.title,
                authors=paper.authors,
                publication_date=paper.published,
                source_url=paper.link,
                full_text=full_text,
                meta={"id": str(paper.id)},
            )
            es_paper.save()
            return True
        except PdfReadError:
            logging.error(f"Error reading pdf: {file_path}")
            return False
        except Exception as e:
            logging.error(f"Error indexing paper: {e}")
            return False

    @staticmethod
    def get_document_with_id(doc_id):
        try:
            es_connection = ESConnection().get_connection()
            s = Search(using=es_connection, index=ResearchPaper.Index.name).query(
                "match", id=str(doc_id)
            )
            response = s.execute()

            if response.hits.total.value > 1:
                raise ValueError(f"Found more than one document with the id {doc_id}")

            return None if response.hits.total.value == 0 else response.hits[0]
        except Exception as e:
            logging.error(f"Error in getting document with ID {doc_id}: {e}")
            return None

    @staticmethod
    def print_all_documents():
        es_connection = ESConnection().get_connection()
        s = Search(using=es_connection, index=ResearchPaper.Index.name).source(includes=[])
        response = s.execute()
        for num, hit in enumerate(response):
            print(num, hit.title)
