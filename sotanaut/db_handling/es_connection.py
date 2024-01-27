import logging

from elasticsearch_dsl import connections


def create_connection():
    connections.create_connection(
        hosts=["http://elastic:vSM1agjn5uU8aRTKMS7G@elasticsearch:9200/"],
    )
    logging.info("Successfully connected to the elastic search")


def get_connection():
    return connections.get_connection()
