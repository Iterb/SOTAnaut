from datetime import datetime
from scholarly import scholarly
from sotanaut.paper_retrieval.models.paper import Paper

class GoogleScholarSource:

    @staticmethod
    def _search_google_scholar(query, max_results=10):
        """Search for papers on Google Scholar."""
        search_query = scholarly.search_pubs(query)
        articles = [next(search_query) for _ in range(max_results)]
        print("Sample article data:", articles[0])  # Print the first article's data
        return articles

    @staticmethod
    def _parse_article(article):
        """Parse article data into a dictionary."""
        bib = article.get('bib', {})
        title = bib.get('title', 'No title available')
        authors = bib.get('author', [])
        published = bib.get('pub_year', 'Unknown year')
        summary = bib.get('abstract', 'No abstract available')
        link = article.get('pub_url', '')

        return {
            "title": title,
            "authors": authors,
            "published": published,
            "summary": summary,
            "link": link,
        }
    # @staticmethod
    # def parse_date_with_placeholder(date_string):
    #     # Define the possible formats
    #     formats = ["%Y-%b-%d", ]
    #     # I get only 
    #     for fmt in formats:
    #         try:
    #             return 
    #         except ValueError:
    #             # Continue to the next format if the current one fails
    #             continue

    #     # If all formats fail, the date format is incorrect
    #     raise ValueError(
    #         "Date format is incorrect. Supported formats: 'YYYY-MMM-DD', 'YYYY-MM-DD', or 'YYYY-MMM-??'."
    #     )

    @staticmethod
    def _translate_to_paper_format(google_scholar_data):
        """Translate Google Scholar-specific data to standardized Paper format."""
        print(google_scholar_data["published"])
        # print(google_scholar_data["title"])
        print(google_scholar_data)
        
        
        return {
            "title": google_scholar_data["title"],
            "authors": google_scholar_data["authors"],
            "date_published": datetime.strptime(f"{google_scholar_data['published']}-01-01", "%Y-%m-%d"), # we get just the year
            "abstract": google_scholar_data["summary"],
            "paper_link": google_scholar_data["link"],
            "source": "google_scholar",
        }

    @staticmethod
    def get_papers(keywords, max_results=10):
        """Retrieve and process papers based on given keywords."""
        query_keywords = " ".join(keywords)  # Keywords are space-separated in Google Scholar searches
        articles = GoogleScholarSource._search_google_scholar(query_keywords, max_results)
        papers_data = [GoogleScholarSource._parse_article(article) for article in articles]
        return [
            Paper(**GoogleScholarSource._translate_to_paper_format(paper_data))
            for paper_data in papers_data
        ]

