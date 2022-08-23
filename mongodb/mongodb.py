import os
import pymongo


def get_all_collections_mongodb():
    client = pymongo.MongoClient(
        str(os.getenv("DATABASE_URL")) + "&" + str(os.getenv("CA_CERT")),
        authSource="admin",
    )
    db = client[os.getenv("MONGO_DB")]
    return db.list_collection_names()


def get_all_portal_ids_in_collection(collection):
    client = pymongo.MongoClient(
        str(os.getenv("DATABASE_URL")) + "&" + str(os.getenv("CA_CERT")),
        authSource="admin",
    )
    db = client[os.getenv("MONGO_DB")]
    list_of_portal_ids = db[collection].distinct("portal_id") + db[collection].distinct("portalId")
    return list(dict.fromkeys(list_of_portal_ids))
