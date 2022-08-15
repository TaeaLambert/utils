import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import pymongo
from program.utils.hubspot.hubspot_api import token_api_request


def write_to_json_overwite(data, path: Path):
    # write data to a json file
    with open(path, "w", encoding="utf8") as outfile:
        json.dump(data, outfile)
    return "done"


### if you want to create properties while installing this app uncomment this and comment the funtion below

def hubspot_login_create_property(code):
    print("login")
    tokens = oauth_login(code)
    if tokens:
        print("saving tokens.....")
        hub = check_access_token(tokens["access_token"])
        tokens["portal_id"] = str(hub["hub_id"])
        save_token_mongodb(tokens)
        print("saved tokens.....")
        return [tokens["access_token"], str(hub["hub_id"])]
    return 400

def hubspot_login(code):
    print("login")
    tokens = oauth_login(code)
    if tokens:
        print("saving tokens.....")
        hub = check_access_token(tokens["access_token"])
        tokens["portal_id"] = str(hub["hub_id"])
        save_token_mongodb(tokens)
        print("saved tokens.....")
        return str(hub["hub_id"])
    return 400


def oauth_login(code):
    print(os.getenv("REDIRECT_URI"))
    url = "https://api.hubapi.com/oauth/v1/token"
    formData = (
        f"grant_type=authorization_code&code={code}"
        + "&redirect_uri="
        + os.getenv("REDIRECT_URI")
        + "&client_id="
        + os.getenv("CLIENT_ID")
        + "&client_secret="
        + os.getenv("CLIENT_SECRET")
    )
    response = token_api_request(url, "POST", data=formData)
    if response.status_code != 400:
        return response.data
    else:
        return None


def check_access_token(access_token):
    url = "https://api.hubapi.com/oauth/v1/access-tokens/" + access_token
    response = token_api_request(url, "GET")
    if response.status_code == 200:
        return response.data
    else:
        return False


def get_access_token(portal_id: int):
    # TODO get access token from mongodb
    tokens = get_tokens_by_portal_id_mongodb(portal_id)
    refresh_token = tokens["refresh_token"]
    formData = (
        "grant_type=refresh_token&client_id="
        + os.getenv("CLIENT_ID")
        + "&client_secret="
        + os.getenv("CLIENT_SECRET")
        + "&redirect_uri="
        + os.getenv("REDIRECT_URI")
        + "&refresh_token="
        + refresh_token
    )
    url = "https://api.hubapi.com/oauth/v1/token"
    new_tokens = token_api_request(url, "POST", data=formData).data
    date_time_plus_25_minutes = datetime.now() + timedelta(minutes=25)
    tokens_for_save = {
        "access_token": new_tokens["access_token"],
        "expires_at": date_time_plus_25_minutes.isoformat(),
    }
    write_to_json_overwite(tokens_for_save, f"./tokens/tokens_{portal_id}.json")
    return new_tokens["access_token"]


def save_token_mongodb(tokens):
    client = pymongo.MongoClient(
        str(os.getenv("DATABASE_URL")) + "&" + str(os.getenv("CA_CERT")),
        authSource="admin",
    )
    db = client[os.getenv("MONGO_DB")]
    collection = db[os.getenv("MONGO_COLLECTION")]
    collection.replace_one({"portal_id": tokens["portal_id"]}, tokens, upsert=True)
    return "done"


def get_tokens_by_portal_id_mongodb(portal_id: str):
    client = pymongo.MongoClient(
        str(os.getenv("DATABASE_URL")) + "&" + str(os.getenv("CA_CERT")),
        authSource="admin",
    )
    db = client[os.getenv("MONGO_DB")]
    collection = db[os.getenv("MONGO_COLLECTION")]
    document = collection.find_one({"portal_id": portal_id})
    return document


def get_all_tokens_mongodb():
    client = pymongo.MongoClient(
        str(os.getenv("DATABASE_URL")) + "&" + str(os.getenv("CA_CERT")),
        authSource="admin",
    )
    db = client[os.getenv("MONGO_DB")]
    collection = db[os.getenv("MONGO_COLLECTION")]
    return collection.find()
