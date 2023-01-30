from datetime import datetime, timedelta
import json
import os
import hmac
from base64 import b64encode
from hashlib import sha256
from fastapi import HTTPException, Header, Request, status

# Imports Python standard library logging
import logging


async def verify_hubspot_signature(request: Request, x_hubspot_signature_v3: str = Header()):
    # print("in verify_hubspot_signature")
    # print(x_hubspot_signature_v3)
    signature = await V3_signature(request)
    if signature == None:
        logging.warning(x_hubspot_signature_v3 != signature)
        logging.warning(x_hubspot_signature_v3)
        logging.warning(signature)
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, detail="This Request is from more than 30 seconds ago")
    elif x_hubspot_signature_v3 != signature:
        logging.warning(x_hubspot_signature_v3 != signature)
        logging.warning(x_hubspot_signature_v3)
        logging.warning(signature)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="The request is not from the right portal.")


async def V3_signature(request: Request):
    hub_time_signature = request.headers["X-HubSpot-Request-Timestamp"]
    if datetime.fromtimestamp(int(hub_time_signature[:-3])) < datetime.now() + timedelta(seconds=-30):
        return None

    client_secret = os.getenv("CLIENT_SECRET")
    request_method = request.method
    uri = str(request.url)
    logging.info(uri)
    if "http://" in uri:
        uri.replace("http", "https")

    if request_method == "POST":
        body = await request.body()
        total_string = request_method + uri + body.decode() + hub_time_signature
        logging.info(total_string)
    else:
        total_string = request_method + uri + hub_time_signature
        logging.info(total_string)

    signature = b64encode(hmac.new(key=bytes(client_secret, "utf-8"), msg=bytes(total_string, "utf-8"), digestmod=sha256).digest()).decode()
    return signature
