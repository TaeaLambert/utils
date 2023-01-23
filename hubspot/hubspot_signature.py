import os
import hmac
from flask import Request
from base64 import b64encode
from hashlib import sha256


def V3_signature(request: Request):
    hub_signature = request.headers["X-HubSpot-Signature-v3"]
    hub_time_signature = request.headers["X-HubSpot-Request-Timestamp"]

    client_secret = os.getenv("CLIENT_SECRET")
    request_method = request.method
    if request_method == "POST":
        uri = (
            "https" + request.host_url.split("http")[1][:-1] + request.full_path
            if "https" not in request.host_url
            else request.host_url[:-1] + request.full_path
        )
        if uri[-1:] == "?":
            uri = uri[:-1]
        total_string = request_method + uri + request.data.decode() + hub_time_signature
    else:
        uri = (
            "https" + request.host_url.split("http")[1][:-1] + request.full_path
            if "https" not in request.host_url
            else request.host_url[:-1] + request.full_path
        )
        total_string = request_method + uri + hub_time_signature

    signature = b64encode(hmac.new(key=bytes(client_secret, "utf-8"), msg=bytes(total_string, "utf-8"), digestmod=sha256).digest()).decode()
    if hub_signature != signature:
        return False
    else:
        return True
