import os
from datetime import datetime, timedelta
from program.utils.hubspot.files import json_to_dict, write_to_json_overwite

BASE_LOCATION = "./cached_responses/"
FILE_FORMAT = {"expiry": datetime.now(), "data": {}}


class cache_workflow_response:

    portal_id: str
    file_name: str
    timeout_duration: timedelta
    time_now: datetime

    expiry_datetime: datetime or bool
    data: dict or bool

    def __init__(
        self,
        portal_id: str,
        file_name: str,
        timeout_duration: timedelta = timedelta(minutes=5),
        time_now: datetime = datetime.now(),
    ):
        self.portal_id = portal_id
        self.file_name = file_name
        self.timeout_duration = timeout_duration
        self.time_now = time_now
        self.file_location = BASE_LOCATION + portal_id + "_" + file_name + ".json"

        if os.path.exists(BASE_LOCATION + portal_id + "_" + file_name + ".json"):
            file_data = json_to_dict(self.file_location)
            self.expiry_datetime = datetime.strptime(file_data["expiry"], "%Y-%m-%dT%H:%M:%S:%fZ")
            self.data = file_data["data"]
        else:
            self.expiry_datetime = False
            self.data = False

    @property
    def has_data(self) -> bool:
        """_summary_

        Does this file contain any data.

        Returns:
            bool: True or False
        """
        if self.data != False:
            return True
        else:
            return False

    @property
    def is_data_fresh(self) -> bool:
        """_summary_

        If the data expiry_datetime is larger then datetime.now() then
        return a True

        If the expiry_datetime is smaller than datetime.now() or the data
        does not exist then this function will return a False

        Returns:
            bool: True or False
        """
        if self.has_data:
            return self.expiry_datetime > self.time_now
        else:
            return False

    def refresh_data(self, data):
        if self.file_location != False:

            self.expiry_datetime = datetime.now() + self.timeout_duration
            write_to_json_overwite(
                {"expiry": self.expiry_datetime.strftime("%Y-%m-%dT%H:%M:%S:%fZ"), "data": data}, self.file_location
            )

            self.data = data
        else:
            return "Somthing went wrong with this class."


# def cache_workflow_response(portal_id:str, response_name:str):
# check if file exists
# portal id
# what response file you need
# date time now
# timeout_duration
# if file exist
# timeout_duration < time now
# return "refresh"
# timeout_duration > time now
# return data
# if file dosent exist
# return "No File"


# if os.path.exists(f"./cached_responses/{portal_id}.json") == True:
#         data = json_to_dict(f"./cached_responses/{portal_id}.json")
#         # TODO:FORMAT date below.
#         if datetime.strptime(data["expire"], "%Y-%m-%dT%H:%M:%S:%fZ") > datetime.now():
#             return data["data"]
#         else:
#             data = get_properties_multi_object_write_only_by_type(access_token, objects, ["string"])
#             now_plus_15_sec = datetime.now() + timedelta(seconds=15)
#             write_to_json_overwite(
#                 {"expire": now_plus_15_sec.strftime("%Y-%m-%dT%H:%M:%S:%fZ"), "data": data},
#                 f"./cached_responses/{portal_id}.json",
#             )
#             return data
#     else:
#         data = get_properties_multi_object_write_only_by_type(access_token, objects, ["string"])
#         now_plus_15_sec = datetime.now() + timedelta(seconds=15)
#         write_to_json_overwite(
#             {"expire": now_plus_15_sec.strftime("%Y-%m-%dT%H:%M:%S:%fZ"), "data": data},
#             f"./cached_responses/{portal_id}.json",
#         )
#         return data
