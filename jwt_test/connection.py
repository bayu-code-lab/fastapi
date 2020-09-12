import sys
import pymongo
import settings

class DbMongoManager(object):
    def __init__(self,collection):
        self.client=pymongo.MongoClient(settings.MONGO_DB_CONNECTION)
        self.db=self.client[settings.MONGO_DB_NAME]
        self.collection=self.db[collection]

    def __enter__(self):
        return self.collection

    def __exit__(self,exc_type, exc_value, exc_traceback):
        self.client.close()