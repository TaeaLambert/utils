from requests import request

from program.utils.pipedrive.pipedrive_response import Pipedrive_response


class Pipedrive_client:

    __api_token: str = ""

    def __init__(self, api_token):
        self.__api_token = api_token

    # Activities
    def get_one_activity(self, id) -> Pipedrive_response:
        url = f"https://api.pipedrive.com/v1/activities/{id}?api_token={self.__api_token}"
        response = Pipedrive_response(request("GET", url))
        return response

    def get_all_activities(self) -> Pipedrive_response:
        url = f"https://api.pipedrive.com/v1/activities?limit=500&start=0&api_token={self.__api_token}"
        response = Pipedrive_response(request("GET", url))
        count = 0
        while response.has_pagination == True:
            pagination_response = Pipedrive_response(request("GET", response.get_pagination_url))
            response.add_pagination_response(pagination_response.data)
            response.response = pagination_response.response
            response.set_url(pagination_response.url)

            count += 1
            print(f"Getting all activities info: Loop({count}) activities({len(response.data)})")
        return response

    def get_all_activities_details(self, data: list[dict]) -> Pipedrive_response:
        response_list = []
        for activity in data:
            response_list.append(self.get_one_activity(activity.get("id")).data)
            if len(response_list) % 10 == 0:
                print(f"Getting activities details: ({len(response_list)}/{len(data)})")
        return response_list

    # Files

    def download_file(self, id, name: str):
        url = f"https://api.pipedrive.com/v1/files/{id}/download?api_token={self.__api_token}"
        file_name = name.split(".")[0]
        response = Pipedrive_response(request("GET", url, stream=True), f"./program/downloaded_files/{file_name}")
        return response

    def get_all_files(self) -> Pipedrive_response:
        url = f"https://api.pipedrive.com/v1/files?limit=500&start=0&api_token={self.__api_token}"
        response = Pipedrive_response(request("GET", url))
        count = 0
        while response.has_pagination == True:
            pagination_response = Pipedrive_response(request("GET", response.get_pagination_url))
            response.add_pagination_response(pagination_response.data)
            response.response = pagination_response.response
            response.set_url(pagination_response.url)

            count += 1
            print(f"Getting all file info: Loop({count}) Files({len(response.data)})")
        return response
