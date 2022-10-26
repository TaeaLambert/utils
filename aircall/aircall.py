import requests


class Aircall_client:
    __base_url: str = ""
    url: str = ""
    response_data: dict = {}

    def __init__(self, access_token) -> None:
        self.__base_url = access_token

    def get_aircall_user_by_email(self, email: str) -> dict:
        url = f"{self.__base_url}/v1/users"
        self.url = "/v1/users"
        try:
            response = requests.get(url)
            self.response_data = response.json()
            for user in response.json()["users"]:
                if user["email"] == email:
                    return user
            return False
        except Exception as e:
            return e

    def get_call_by_id(self, call_id: str) -> dict:
        url = f"{self.__base_url}/v1/calls/{call_id}"
        self.url = f"/v1/calls/{call_id}"
        try:
            response = requests.get(url)
            self.response_data = response.json()
            return response.json()
        except Exception as e:
            return e

    def transfer_call(self, call_id, user_id):
        url = f"{self.__base_url}/v1/calls/{call_id}/transfers"
        data = {"user_id": user_id}
        self.url = f"/v1/calls/{call_id}/transfers"
        try:
            self.response_data = requests.post(url, data=data).json()
        except Exception as e:
            return e

    def __str__(self):
        return f"Last url call: {self.url}\n\nLast api response: {str(self.response_data)}"
