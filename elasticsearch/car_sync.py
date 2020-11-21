from elasticsearch import Elasticsearch, helpers
from query import get_car_list
import uuid
es = Elasticsearch('https://search-bidbox-es-staging-avieipaq3q7okk6cqyc264mlby.ap-southeast-1.es.amazonaws.com', http_auth=('bidboxadmin', 'Bidboxdev123!'))

data = get_car_list()
actions = [
    {
        "_id" : doc['price_id'], # random UUID for _id
        "_type" : "_doc", # document _type
        "_source": {
                    'brand' : doc['brand'],
                    'model' : doc['model'],
                    'variant' : doc['variant'],
                    'sku' : doc['sku'],
                    'is_sku_default' : doc['is_sku_default'],
                    'location' : doc['location'],
                    'is_location_default' : doc['is_location_default'],
                    'otr' : doc['otr'],
                    'discount' : doc['discount'],
                    'otr_nett' : doc['otr_nett'],
                    'finance_service' : doc['finance_service'],
                    'monthly_installment' : doc['monthly_installment'],
                    'cc_kendaraan' : doc['cc_kendaraan'],
                    'transmission' : doc['transmission'],
                    'fuel' : doc['fuel'],
                    'variant_img_url' : doc['variant_img_url'],
                    'keyword': doc['keyword'],
                    'brand_id' : doc['brand_id'],
                    'model_id' : doc['model_id'],
                    'variant_id' : doc['variant_id'],
                    'sku_id' : doc['sku_id'],
                    'price_id' : doc['price_id'],
                    'simulation_id' : doc['simulation_id'],
                    'finance_service_id' : doc['finance_service_id'],
                    'location_id' : doc['location_id'],
                    'transmission_id' : doc['transmission_id'],
                    'fuel_id' : doc['fuel_id']
                    }
    }
    for doc in data #loop data
]
try:
    # make the bulk call using 'actions' and get a response
    response = helpers.bulk(es, actions, index='bidbox_new_car_list', doc_type='_doc')
    print ("\nactions RESPONSE:", response)
except Exception as e:
    print("\nERROR:", e)
