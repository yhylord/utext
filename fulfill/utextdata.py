from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
import os

http_auth = os.environ['UTEXT_NAME'] + ":" + os.environ['UTEXT_PSWD']
client = Elasticsearch("https://utext.club", http_auth=http_auth, use_ssl=True)
#client = Elasticsearch("https://es.utext.club", http_auth=http_auth, use_ssl=True, verify_certs=True)
client.ping()


def get_relevent_documents(terms):

    query_terms = " ".join(terms)
    q = Q("multi_match", query=query_terms, fields=['name', 'content'])
    
    s = Search(using=client, index="documents").query(q)
    resp = s.execute()

    docs = [ hit for hit in resp['hits']['hits'] ]

    return docs
