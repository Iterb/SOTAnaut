from datetime import datetime

class Paper:
    DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'  # ISO format as seen in the sample

    def __init__(self, title, authors, date_published, abstract, paper_link):
        self.title = title
        self.authors = authors
        self.published = datetime.strptime(date_published, self.DATE_FORMAT)
        self.summary = abstract
        self.link = paper_link

    def __str__(self):
        return f"Title: {self.title}\nAuthors: {', '.join(self.authors)}\nPublished: {self.published.strftime('%Y-%m-%d')}\nSummary: {self.summary[:100]}...\nLink: {self.link}"

    def get_age_in_days(self):
        """Returns the age of the paper in days."""
        return (datetime.now() - self.published).days

    def is_recent(self, threshold=365):
        """Determines if the paper is 'recent' based on a given threshold in days."""
        return self.get_age_in_days() <= threshold