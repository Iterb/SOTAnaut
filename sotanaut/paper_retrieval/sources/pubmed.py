from datetime import datetime

from Bio import Entrez

from sotanaut.paper_retrieval.models.paper import Paper


class PubmedSource:
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

    Entrez.email = "sebastian.puchala.95@gmail.com"  # Set your email here

    @staticmethod
    def _search_pubmed(query, max_results=10):
        """Interact with the PubMed API and return the article IDs."""
        handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
        results = Entrez.read(handle)
        handle.close()
        return results["IdList"]

    @staticmethod
    def _fetch_details(id_list):
        """Fetch details of PubMed articles based on their IDs."""
        ids = ",".join(id_list)
        handle = Entrez.efetch(db="pubmed", retmode="xml", id=ids)
        results = Entrez.read(handle)
        handle.close()
        return results

    @staticmethod
    def _parse_article(article):
        """Parse article data into a dictionary."""
        article_data = article["MedlineCitation"]["Article"]
        title = article_data.get("ArticleTitle", "No title available")
        authors = [
            author["ForeName"] + " " + author["LastName"]
            for author in article_data.get("AuthorList", [])
        ]
        pub_date = article_data["Journal"]["JournalIssue"]["PubDate"]
        date_published = f"{pub_date.get('Year', '????')}-{pub_date.get('Month', '??')}-{pub_date.get('Day', '??')}"
        abstract = article_data.get("Abstract", {}).get("AbstractText", [""])[0]
        link = f"https://pubmed.ncbi.nlm.nih.gov/{article['MedlineCitation']['PMID']}/"
        # link = f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{article['MedlineCitation']['PMID']}/"

        return {
            "title": title,
            "authors": authors,
            "published": date_published,
            "summary": abstract,
            "link": link,
        }

    @staticmethod
    def parse_date_with_placeholder(date_string):
        # Define the possible formats
        formats = ["%Y-%b-%d", "%Y-%m-%d"]

        for fmt in formats:
            try:
                # Replace '??' with '01' in case the day is missing, then try to parse
                return datetime.strptime(date_string.replace("??", "01"), fmt)
            except ValueError:
                # Continue to the next format if the current one fails
                continue

        # If all formats fail, the date format is incorrect
        raise ValueError(
            "Date format is incorrect. Supported formats: 'YYYY-MMM-DD', 'YYYY-MM-DD', or 'YYYY-MMM-??'."
        )

    @staticmethod
    def _translate_to_paper_format(pubmed_data):
        """Translate PubMed-specific data to standardized Paper format."""
        return {
            "title": pubmed_data["title"],
            "authors": pubmed_data["authors"],
            "date_published": PubmedSource.parse_date_with_placeholder(pubmed_data["published"]),
            "abstract": pubmed_data["summary"],
            "paper_link": pubmed_data["link"],
            "source": "pubmed",
        }

    @staticmethod
    def get_papers(keywords, max_results=10):
        """Retrieve and process papers based on given keywords."""
        query_keywords = " OR ".join(keywords)  # Joining keywords with AND for PubMed search
        ids = PubmedSource._search_pubmed(query_keywords, max_results)
        articles = PubmedSource._fetch_details(ids)["PubmedArticle"]
        papers_data = [PubmedSource._parse_article(article) for article in articles]
        return [
            Paper(**PubmedSource._translate_to_paper_format(paper_data))
            for paper_data in papers_data
        ]
