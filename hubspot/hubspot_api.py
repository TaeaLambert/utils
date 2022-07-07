from time import sleep
from typing import Literal
import requests
from program.utils.hubspot.hubspot_api_exection import (
    HubspotAPIError,
    HubspotAPILimitReached,
)


class HubspotResponse:
    data: dict

    def __init__(self, response: requests.Response) -> None:
        if response.status_code >= 200 and response.status_code <= 299:
            self.data = response.json()
        else:
            if response.status_code == 413:
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
        return hubspot_request(self.results["paging"]["next"]["link"])

    def get_all_results(self) -> dict:
        """all_results is using the has_pagination property to deternine if there is another
        request that needs to be done to get all the results. It is recursive and will stop
        only when there is no nore pages to the current request"""
        all_results = [self.results]
        current_response = self
        while current_response.has_pagination:
            current_response = self.next()
            all_results.append(current_response.results)

        return all_results


def hubspot_request(url: str, verb: Literal["GET", "POST", "PUT"] = "GET", nb_retry=0) -> HubspotResponse:
    access_token = "asdasdasd"
    header = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer " + access_token,
    }
    try:
        response = requests.get(url, headers=header)
    except HubspotAPILimitReached:
        if nb_retry > 10:
            raise HubspotAPILimitReached(f"After {nb_retry} we are still getting errors", 413)
        sleep(5)
        hubspot_request(url, verb, nb_retry + 1)

    return HubspotResponse(response)
