import os
from datetime import datetime, timedelta
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError


class mongo_client:
    def __init__(self) -> None:
        self.client = MongoClient(str(os.getenv("DATABASE_URL")) + "&" + str(os.getenv("CA_CERT")), authSource="admin")

        self.db = self.client[os.getenv("MONGO_DB")]
        self.collection = self.db[os.getenv("MONGO_DATA_COLLECTION")]
        self.timeout = datetime.now() + timedelta(minutes=15)

    def save_object_increment_code_mongodb(self, portal_id, object_type, prop_to_set, data):
        try:
            self.collection.find_one_and_update(
                {"portal_id": portal_id}, {"$set": {"objects": {object_type: {prop_to_set: data}}}}, upsert=True
            )
        except ServerSelectionTimeoutError as err:
            # do whatever you need
            print(err)
            return 400

    def get_object_increment_code_mongodb(self, portal_id, object_type, prop_to_set):
        try:
            document: dict = self.collection.find_one({"portal_id": portal_id})
            return document.get("objects").get(object_type).get(prop_to_set)
        except ServerSelectionTimeoutError as err:
            # do whatever you need
            print(err)
            return 400
