import requests
import urllib.parse as urlparse
from program.utils.pipedrive.pipedrive_api_execution import Pipedrive_api_error


class Pipedrive_response:

    response: dict = {}
    url: str = ""
    data: list[dict]
    status_code: int
    file_name: str = ""

    def __init__(self, response: requests.Response, file_name: str = "") -> None:
        if response.status_code >= 200 and response.status_code <= 299:
            self.url = response.url
            if "files/" in response.url:
                with open(f"{file_name}.pdf", "wb") as f:
                    f.write(response.content)
            else:
                self.response = response.json()
                self.data = self.response["data"]
        else:
            raise Pipedrive_api_error(
                response.text if response.text != "" else response.reason,
                response.status_code,
            )

    @property
    def has_pagination(self):
        if "additional_data" in self.response:
            if self.response["additional_data"]["pagination"]["more_items_in_collection"] == True:
                return True
        else:
            return False

    @property
    def get_pagination_url(self):
        if self.has_pagination == False:
            return None
        new_url = urlparse.urlparse(self.url)
        params = urlparse.parse_qs(new_url.query)
        params["start"] = int(params["start"][0]) + 500
        params["limit"] = int(params["limit"][0])
        params["api_token"] = params["api_token"][0]
        res = urlparse.ParseResult(
            scheme=new_url.scheme,
            netloc=new_url.hostname,
            path=new_url.path,
            params=new_url.params,
            query=urlparse.urlencode(params),
            fragment=new_url.fragment,
        )
        return res.geturl()

    def add_pagination_response(self, data):
        self.data = data + self.data

    def set_url(self, url):
        self.url = url

    def set_response(self, data):
        self.response = data
