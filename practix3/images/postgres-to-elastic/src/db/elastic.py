from elasticsearch import Elasticsearch


def get_elastic() -> Elasticsearch:
    return Elasticsearch('http://elastic:9200')
