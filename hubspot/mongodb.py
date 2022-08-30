import os
import pymongo


def save_token_mongodb(tokens):
    """_summary_
    This funtion is used to save a new set of tokens (refresh, access) to the selected DB in the .env file

    Args:
        tokens (_type_): set of tokens gathered from the oauth_login funtion

    Example of data saved::

        {
            "token_type" : "bearer"
            "refresh_token" : ""
            "access_token" : ""
            "expires_in" : 1800
            "portal_id" : "########"
        }
    """
    client = pymongo.MongoClient(
        str(os.getenv("DATABASE_URL")) + "&" + str(os.getenv("CA_CERT")),
        authSource="admin",
    )
    db = client[os.getenv("MONGO_DB")]
    collection = db[os.getenv("MONGO_COLLECTION")]
    collection.replace_one({"portal_id": tokens["portal_id"]}, tokens, upsert=True)


def get_tokens_by_portal_id_mongodb(portal_id: str):
    """_summary_
    This funtion get a set of tokens within the selected DB (.env file) using the portal id as a queary parameter

    Args:
        portal_id (str): Portal id of the portal that triggered this application.

     Example::

        {
            "token_type" : "bearer"
            "refresh_token" : ""
            "access_token" : ""
            "expires_in" : 1800
            "portal_id" : "########"
        }


    Returns:
        dict: This contains all the tokens assoicatied to this portal id passed in.
    """
    client = pymongo.MongoClient(
        str(os.getenv("DATABASE_URL")) + "&" + str(os.getenv("CA_CERT")),
        authSource="admin",
    )
    db = client[os.getenv("MONGO_DB")]
    collection = db[os.getenv("MONGO_COLLECTION")]
    document = collection.find_one({"portal_id": portal_id})
    return document
