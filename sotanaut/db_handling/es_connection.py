import logging

from elasticsearch_dsl import connections


class ESConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.create_connection()
        return cls._instance

    def create_connection(self):
        connections.create_connection(
            hosts=["http://elastic:vSM1agjn5uU8aRTKMS7G@elasticsearch:9200/"]
        )
        logging.info("Successfully connected to Elasticsearch")

    @staticmethod
    def get_connection():
        return connections.get_connection()
