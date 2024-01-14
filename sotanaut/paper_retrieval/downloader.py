# downloader.py
import logging
import os
import re
from pathlib import Path

import requests
from metapub import FindIt


class PaperDownloader:
    def __init__(self, paper):
        self.paper = paper
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

    def download_paper(self, folder_path):
        try:
            if download_url := self._get_download_url():
                file_path = self._download_and_save_pdf(download_url, folder_path)
            else:
                logging.error(f"No download URL found for: {self.paper.title}")
                return None
        except requests.RequestException as e:
            logging.error(f"Error downloading the paper '{self.paper.title}': {e}")
            return None

        return file_path

    def _get_download_url(self):
        if self.paper.source == "pubmed":
            return self._get_pubmed_url()
        elif self.paper.source == "arxiv":
            return self._get_arxiv_url()
        else:
            return self.paper.link

    def _get_pubmed_url(self):
        match = re.search(r"\d+", self.paper.link)
        pmid = int(match[0]) if match else None
        if pmid:
            src = FindIt(pmid)
            return src.url
        return None

    def _get_arxiv_url(self):
        if match := re.search(r"arxiv\.org/abs/(\d+\.\d+)", self.paper.link):
            paper_id = match[1]
            return f"https://arxiv.org/pdf/{paper_id}.pdf"
        return None

    def _download_and_save_pdf(self, url, folder_path):
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        file_path = os.path.join(folder_path, f"{self.paper.id}.pdf")
        with open(file_path, "wb") as file:
            file.write(response.content)
        logging.info(f"Paper downloaded successfully: {file_path}")

        return file_path
