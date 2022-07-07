from datetime import datetime, timedelta
from http import client
from telnetlib import TLS
from urllib import response
import requests
import os
import pymongo

from utils.files import write_to_json


def hubspot_login(code):
    print("login")
    tokens = oauth_login(code)
    if not tokens:
        return 400
    print("saving tokens.....")
    hub = check_access_token(tokens["access_token"])
    tokens["portal_id"] = str(hub["hub_id"])
    save_token_mongodb(tokens)
    print("saved tokens.....")
    return str(hub["hub_id"])


def oauth_login(code):
    print(os.getenv("REDIRECT_URI"))
    formdata = (
        f"grant_type=authorization_code&code={code}"
        + "&redirect_uri="
        + os.getenv("REDIRECT_URI")
        + "&client_id="
        + os.getenv("CLIENT_ID")
        + "&client_secret="
        + os.getenv("CLIENT_SECRET")
    )
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    url = "https://api.hubapi.com/oauth/v1/token?"
    response = requests.post(url, data=formdata, headers=headers)
    print(response.json())
    if response.status_code == 200:
        return response.json()
    else:
        return None


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
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=formData, headers=headers)
    new_tokens = response.json()
    date_time_plus_25_minutes = datetime.now() + timedelta(minutes=25)

    tokens_for_save = {"access_token": new_tokens["access_token"], "expires_at": date_time_plus_25_minutes}
    write_to_json(tokens_for_save, f"/tokens/tokens_{portal_id}.json")

    # token_{portal_id}.json
    # if file does not exists then access token is invalid
    # {"access_token": "asdasdasdsda", "expires_at": "123123123"}
    # check if expires_at is less than 5min in the future
    # if not use access token
    # if less than 5min refresh the access token and save it on disk with the new expires_at


def check_access_token(access_token):

    url = "https://api.hubapi.com/oauth/v1/access-tokens/" + access_token
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return False


def save_token_mongodb(tokens):
    client = pymongo.MongoClient(
        str(os.getenv("DATABASE_URL")) + "&" + str(os.getenv("CA_CERT")),
        authSource="admin",
    )
    db = client[os.getenv("MONGO_DB")]
    collection = db[os.getenv("MONGO_COLLECTION")]
    collection.insert_one(tokens)
    return "done"


def get_tokens_by_portal_id_mongodb(portal_id: str):
    client = pymongo.MongoClient(
        str(os.getenv("DATABASE_URL")) + "&" + str(os.getenv("CA_CERT")),
        authSource="admin",
    )
    db = client[os.getenv("MONGO_DB")]
    collection = db[os.getenv("MONGO_COLLECTION")]
    return collection.find({"portalId": portal_id})


def get_all_tokens_mongodb():
    client = pymongo.MongoClient(
        str(os.getenv("DATABASE_URL")) + "&" + str(os.getenv("CA_CERT")),
        authSource="admin",
    )
    db = client[os.getenv("MONGO_DB")]
    collection = db[os.getenv("MONGO_COLLECTION")]
    return collection.find()
