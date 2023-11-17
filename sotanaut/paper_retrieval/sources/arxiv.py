import requests
import feedparser
from sotanaut.paper_retrieval.models.paper import Paper

class ArxivSource:
    BASE_URL = "http://export.arxiv.org/api/query?"

    @staticmethod
    def _search_arxiv(query):
        """Interact with the arXiv API and return the content."""
        response = requests.get(ArxivSource.BASE_URL + query)
        if response.status_code == 200:
            return response.content
        else:
            response.raise_for_status()

    @staticmethod
    def _parse_feed(content):
        """Parse the Atom feed content into a list of paper data."""
        feed = feedparser.parse(content)
        papers = []
        for entry in feed.entries:
            paper = {
                'title': entry.title,
                'authors': [author.name for author in entry.authors],
                'published': entry.published,
                'summary': entry.summary,
                'link': entry.link
            }
            papers.append(paper)
        return papers
    
    @staticmethod
    def _translate_to_paper_format(arxiv_data):
        """Translate arXiv-specific data to standardized Paper format."""
        return {
            'title': arxiv_data['title'],
            'authors': arxiv_data['authors'],
            'date_published': arxiv_data['published'],
            'abstract': arxiv_data['summary'],
            'paper_link': arxiv_data['link']
        }
    
    @staticmethod
    def get_papers(keywords, max_results=10):
        """Retrieve and process papers based on given keywords."""
        query_keywords = '+OR+'.join(keywords)  # Joining keywords with OR to expand the search
        query = f'search_query=all:{query_keywords}&start=0&max_results={max_results}'
        content = ArxivSource._search_arxiv(query)
        papers_data = ArxivSource._parse_feed(content)
        return [
            Paper(**ArxivSource._translate_to_paper_format(paper_data))
            for paper_data in papers_data
        ]
    