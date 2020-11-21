import requests
from requests.auth import HTTPBasicAuth
import json
# from elasticsearch import Elasticsearch
base_url = "https://search-bidbox-es-staging-avieipaq3q7okk6cqyc264mlby.ap-southeast-1.es.amazonaws.com"

query="""
    {
        "query":{
            "match":{
                "brand":"toyota"
            }
        }
    }
    """
res = requests.post('{}{}{}'.format(base_url,'/bidbox_car_list', '/_search'), json=json.loads(query), auth=HTTPBasicAuth('bidboxadmin','Bidboxdev123!'))
data = json.loads(res.text)
# print(data['hits']['hits'])
for a in data['hits']['hits']:
    print(a['_source'])
# if data['found']:
#     print(data['_source'])
# else:
#     print('Not found!')

# es = Elasticsearch('https://search-bidbox-es-staging-avieipaq3q7okk6cqyc264mlby.ap-southeast-1.es.amazonaws.com', http_auth=('bidboxadmin', 'Bidboxdev123!'))


