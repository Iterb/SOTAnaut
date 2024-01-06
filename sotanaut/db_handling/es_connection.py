from elasticsearch_dsl import connections


def create_connection():
    connections.create_connection(
        hosts=["https://elastic:vSM1agjn5uU8aRTKMS7G@localhost:9200/"],
        verify_certs=False,  # Disable certificate verification
    )


def get_connection():
    return connections.get_connection()
