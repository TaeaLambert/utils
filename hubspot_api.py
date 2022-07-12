from datetime import datetime
import os
from time import sleep
from typing import Literal
import requests
from program.utils.files import json_to_dict
from program.utils.hubspot_api_exection import (
    HubspotAPIError,
    HubspotAPILimitReached,
)
from program.utils.hubspot_oauth import get_access_token

# TODO comments


class HubspotResponse:
    data: dict

    def __init__(self, response: requests.Response, access_token: str) -> None:
        self.access_token = access_token
        # raise HubspotAPILimitReached(response.text, response.status_code)
        if response.status_code >= 200 and response.status_code <= 299:
            self.data = response.json()
        else:
            if response.status_code == 429:
                raise HubspotAPILimitReached(response.text, response.status_code)
            raise HubspotAPIError(response.text, response.status_code)

    @property
    def results(self) -> dict:
        return self.data["results"]

    @property
    def has_pagination(self) -> bool:
        return "paging" in self.data

    def next(self) -> "HubspotResponse":
        if not self.has_pagination:
            raise HubspotAPIError("No pagination but calling next!", 400)

        return hubspot_request(self.access_token, self.data["paging"]["next"]["link"])

    def get_all_results(self) -> dict:
        """all_results is using the has_pagination property to deternine if there is another
        request that needs to be done to get all the results. It is recursive and will stop
        only when there is no nore pages to the current request"""
        all_results = self.results
        current_response = self
        while current_response.has_pagination:
            current_response = self.next()
            for result in current_response.results:
                all_results.append(result)

        return {"results": all_results}


def hubspot_request(
    access_token: str,
    url: str,
    verb: Literal["GET", "POST", "PUT", "PATCH"] = "GET",
    nb_retry=0,
    **kwargs,
) -> HubspotResponse:
    header = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer " + access_token,
    }
    try:
        match verb:
            case "GET":
                response = requests.get(url, headers=header)
                response = HubspotResponse(response, access_token)
                return response
            case "POST":
                response = requests.post(url, headers=header, json=kwargs.get("data", {}))
                response = HubspotResponse(response, access_token)
                return response
            case "PUT":
                response = requests.put(url, headers=header, json=kwargs.get("data", {}))
                response = HubspotResponse(response, access_token)
                return response
            case "PATCH":
                response = requests.patch(url, headers=header, json=kwargs.get("data", {}))
                response = HubspotResponse(response, access_token)
                return response
    except HubspotAPILimitReached:
        if nb_retry > 10:
            raise HubspotAPILimitReached(f"After {nb_retry} we are still getting errors", 429)
        print("sleeping for 5 seconds")
        sleep(5)
        print("retrying")
        return hubspot_request(access_token, url, verb, nb_retry + 1, **kwargs)


def get_local_access_token(portal_id):
    if os.path.isfile(f"./tokens/tokens_{portal_id}.json"):
        print("found local tokens")
        date_now = datetime.now()
        local_tokens = json_to_dict(f"./tokens/tokens_{portal_id}.json")
        datetime_object = datetime.fromisoformat(local_tokens["expires_at"])
        if date_now > datetime_object:
            return get_access_token(portal_id)
        return local_tokens["access_token"]
    else:
        return get_access_token(portal_id)
