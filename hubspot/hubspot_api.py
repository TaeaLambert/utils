import json
import os
import logging
from time import sleep
import pathlib as Path
from typing import Literal
import requests
import sentry_sdk
from datetime import datetime
from program.utils.hubspot.hubspot_api_exection import (
    HubspotAPIError,
    HubspotAPILimitReached,
)
from program.utils.hubspot.hubspot_oauth import get_access_token

# TODO comments


class HubspotResponse:
    #  TODO finnish this comments
    """_summary_

    Veriables:
        data: this contains data from hubspot only if the request is successfully completed
        status_code: status code of the response from hubspot


    Raises:
        HubspotAPILimitReached: If the api limit of the funtion that uses this class is hit 10 times in a row then this class will throw this exception :func:`<program.utils.hubspot.hubspot_api_exection.HubspotAPILimitReached>`
        HubspotAPIError: If the http request has any error with the repsponse or request the class will throw this exception :func:`<program.utils.hubspot.hubspot_api_exection.HubspotAPIError>`

    Returns:
        _type_: HubspotResponse This has no default return so you have to select a funtion or property.
    """

    data: dict
    status_code: int

    def __init__(self, response: requests.Response, access_token: str) -> None:
        self.access_token = access_token
        self.status_code = response.status_code
        # raise HubspotAPILimitReached(response.text, response.status_code)
        if response.status_code >= 200 and response.status_code <= 299:
            self.data = response.json()
        else:
            logging.debug(f"{response.text}, {response.status_code}")

            if response.status_code == 429:
                raise HubspotAPILimitReached(response.text, response.status_code)
            raise HubspotAPIError(response.text if response.text != "" else response.reason, response.status_code)

    @property
    def results(self) -> dict:
        """_summary_

        This Returns a list contained in a api request if mutiple items are requested.

        You sould be using :func:`get_all_results()` funtion of this class as this makes
        sure you are not missing any records if the response has paging

         Example::
            {"results":[
                {
                    "key":"value",
                    "key":"value",
                    "properties":{
                    "key":"value",
                    "key":"value",
                    "key":"value"
                    }
                },
                {
                    "key":"value",
                    "key":"value",
                    "properties":{
                    "key":"value",
                    "key":"value",
                    "key":"value"
                    }
                },
                {
                    "key":"value",
                    "key":"value",
                    "properties":{
                    "key":"value",
                    "key":"value",
                    "key":"value"
                    }
                },
            ]}


        Returns:
            dict: returns a dict that contains a list of dict's
        """
        return self.data

    @property
    def has_pagination(self) -> bool:
        """_summary_

        Returns:
            bool: if the api request has more records (only 1000 records per request)
        """
        return "paging" in self.data

    def next(self) -> "HubspotResponse":
        """_summary_

        Raises:
            HubspotAPIError: A error if no paging is found in the resoponse

        Returns:
            HubspotResponse: A hubspot request that contains the text set of data if "paging is found in the response"
        """
        if not self.has_pagination:
            raise HubspotAPIError("No pagination but calling next!", 400)

        return hubspot_request(self.access_token, self.data["paging"]["next"]["link"])

    def get_all_results(self) -> dict:
        """_summary_:
        all_results is using the has_pagination property to deternine if there is another
        request that needs to be done to get all the results. It is recursive and will stop
        only when there is no nore pages to the current request

        Example::

            {"results":
              [
                {
                  "key":"value",
                  "key":"value",
                  "properties":{
                    "key":"value",
                    "key":"value",
                    "key":"value"
                    }
                },
                {
                  "key":"value",
                  "key":"value",
                  "properties":{
                    "key":"value",
                    "key":"value",
                    "key":"value"
                    }
                },
                {
                  "key":"value",
                  "key":"value",
                  "properties":{
                    "key":"value",
                    "key":"value",
                    "key":"value"
                    }
                },
              ]
            }

        Returns:
            dict:
        """

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
    #  TODO finnish this comments
    """_summary_

    Args:
        access_token (str): _description_
        url (str): _description_
        verb (Literal[&quot;GET&quot;, &quot;POST&quot;, &quot;PUT&quot;, &quot;PATCH&quot;], optional): _description_. Defaults to "GET".
        nb_retry (int, optional): _description_. Defaults to 0.

    Raises:
        HubspotAPILimitReached: _description_

    Returns:
        HubspotResponse: _description_
    """
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
            logging.error(f"After {nb_retry} we are still getting errors")
            raise HubspotAPILimitReached(f"After {nb_retry} we are still getting errors", 429)
        logging.info("sleeping for 5 seconds")
        sleep(5)
        logging.info("retrying")
        return hubspot_request(access_token, url, verb, nb_retry + 1, **kwargs)


def get_local_access_token(portal_id: str) -> str:
    #  TODO finnish this comments
    """_summary_

    Args:
        portal_id (str): _description_

    Returns:
        str: _description_
    """
    if os.path.isfile(f"./tokens/tokens_{portal_id}.json"):
        date_now = datetime.now()
        local_tokens = json_to_dict(f"./tokens/tokens_{portal_id}.json")
        datetime_object = datetime.fromisoformat(local_tokens["expires_at"])
        if date_now > datetime_object:
            return get_access_token(portal_id)
        return local_tokens["access_token"]
    else:
        return get_access_token(portal_id)


def token_api_request(
    url: str,
    verb: Literal["GET", "POST"] = "GET",
    nb_retry=0,
    **kwargs,
) -> HubspotResponse:
    #  TODO finnish this comments
    """_summary_

    Args:
        url (str): _description_
        verb (Literal[&quot;GET&quot;, &quot;POST&quot;], optional): _description_. Defaults to "GET".
        nb_retry (int, optional): _description_. Defaults to 0.

    Raises:
        HubspotAPILimitReached: _description_

    Returns:
        HubspotResponse: _description_
    """
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    try:
        match verb:
            case "POST":
                response = requests.post(url, headers=header, data=kwargs.get("data", {}))
                response = HubspotResponse(response, "ss")
                return response
            case "GET":
                response = requests.get(url, headers=header)
                response = HubspotResponse(response, "ss")
                return response
    except HubspotAPILimitReached:
        if nb_retry > 10:
            logging.error(f"After {nb_retry} we are still getting errors")
            raise HubspotAPILimitReached(f"After {nb_retry} we are still getting errors", 429)
        logging.info("sleeping for 5 seconds")
        sleep(5)
        logging.info("retrying")
        return token_api_request(url, verb, nb_retry + 1, **kwargs)
    except HubspotAPIError as e:
        sentry_sdk.capture_exception(e)
        return response


def json_to_dict(path: Path):
    #  TODO finnish this comments
    """_summary_

    Args:
        path (Path): _description_

    Returns:
        _type_: _description_
    """
    with open(path, encoding="utf-8") as f:
        return json.load(f)
