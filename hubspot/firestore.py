import os
import settings

# import pymongo


def save_token_firestore(tokens):
    firestore_collection = settings.get_firestore_client().collection(os.getenv("COLLECTION"))
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

    try:
        firestore_collection.document(tokens["portal_id"]).set(tokens)
    except Exception as e:
        return e


def get_tokens_by_portal_id_firestore(portal_id: str):
    firestore_collection = settings.get_firestore_client().collection(os.getenv("COLLECTION"))
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

    if firestore_collection.document(portal_id).get().exists:
        return firestore_collection.document(portal_id).get().to_dict()
    else:
        return "Not Found"


def get_tokens_by_microapp():
    firestore_collection = settings.get_firestore_client().collection(os.getenv("COLLECTION"))
    tokens_stored = firestore_collection.get()
    portals = []
    for token in tokens_stored:
        portal_id = token._data["portal_id"]
        portals.append(portal_id)
    return portals
