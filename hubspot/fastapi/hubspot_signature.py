import json
import os
import hmac
from base64 import b64encode
from hashlib import sha256
from fastapi import HTTPException, Header, Request


async def verify_hubspot_signature(request: Request, x_hubspot_signature_v3: str = Header()):
    # print("in verify_hubspot_signature")
    # print(x_hubspot_signature_v3)
    signature = await V3_signature(request)
    if x_hubspot_signature_v3 != signature:
        raise HTTPException(status_code=401, detail="The request is not from the right portal.")


async def V3_signature(request: Request):
    hub_time_signature = request.headers["X-HubSpot-Request-Timestamp"]
    client_secret = os.getenv("CLIENT_SECRET")
    request_method = request.method
    if request_method == "POST":
        uri = str(request.url)
        body = await request.body()
        total_string = request_method + uri + body.decode() + hub_time_signature
    else:
        uri = str(request.url)
        total_string = request_method + uri + hub_time_signature

    signature = b64encode(hmac.new(key=bytes(client_secret, "utf-8"), msg=bytes(total_string, "utf-8"), digestmod=sha256).digest()).decode()
    return signature
