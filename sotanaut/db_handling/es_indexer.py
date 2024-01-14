import logging

from elasticsearch_dsl import Date, Document, Text

from sotanaut.db_handling.pdf_extractor import extract_text_from_pdf


# Define a document structure for Elasticsearch
class ResearchPaper(Document):
    id = Text()  # Add the UUID field
    title = Text()
    authors = Text()
    publication_date = Date()
    source_url = Text()
    full_text = Text()

    class Index:
        name = "research-papers"


# Create the index in Elasticsearch if it doesn't exist
from elasticsearch.exceptions import NotFoundError
from PyPDF2.errors import PdfReadError


def index_paper_to_elasticsearch(paper, file_path):
    # Extract text from the PDF
    try:
        full_text = extract_text_from_pdf(file_path)
    except PdfReadError:
        logging.error(f"Error reading pdf: {file_path}")
        return False
    # Create an instance of the ResearchPaper document
    es_paper = ResearchPaper(
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


def ensure_elasticsearch_initialized():
    try:
        # Check if index exists and has the correct mappings
        if not ResearchPaper._index.exists():
            ResearchPaper.init()
    except NotFoundError:
        # Index doesn't exist, so initialize it
        ResearchPaper.init()
