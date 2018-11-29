from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
import os

http_auth = os.environ['UTEXT_NAME'] + ":" + os.environ['UTEXT_PSWD']
client = Elasticsearch("https://utext.club", http_auth=http_auth, use_ssl=True, verify_certs=True)
client.ping()

# just a bunch of kwords to hit parts of dataset
terms = "university scholarship tuition textbooks books party \
        finals grades ta labs office hours health allergies shots \
        bike help services ut austin medical utpd student care\
        people assault classes ida nurse technology food jester government\
        drugs clubs organizations free tutoring grants paper supplies\
        gpa rank honor societies alcohol alumni natural science\
        career apps resume learning jobs "

vocab = set()

for term in terms.split(" "):

    q = Q("multi_match", query=term, fields=['name', 'content'])
    
    s = Search(using=client, index="documents").query(q)
    resp = s.execute()

    docs = [ hit for hit in resp['hits']['hits'] ]

    for doc in docs:
        data = " ".join(doc['_source']['content'])

    words = data.replace('-', ' ').replace(':', ' ').replace('}', '').replace(';', ' ').replace('@', ' ').replace('/', ' ').replace('  ', ' ').replace('www.', '').replace('http://', '').replace('https://', '').split(' ')
    
    for word in words:
        
        if len(word) == 0:
            continue
        if word.startswith('_'):
            continue
        if word.startswith('\''):
            word = word.replace('\'', '')
            
        vocab.add(word.replace('(', '')
                      .replace(')', '')
                      .replace('.', '')
                      .replace(',', '')
                      .replace('?', '')
                      .replace('!', '')
                      .replace('"', '')
                      .replace('*', ''))

with open(os.path.join('qa-model', 'vocab.txt'), 'w') as v:
    v.write("\n".join(sorted(vocab)))
