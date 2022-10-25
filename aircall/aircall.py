import requests


class Aircall_client:
    __base_url: str = ""

    def __init__(self, access_token) -> None:
        self.__base_url = access_token

    def get_aircall_user_by_email(self, email: str) -> dict:
        url = f"{self.__base_url}/v1/users"
        try:
            response = requests.get(url)
            for user in response.json()["users"]:
                if user["email"] == email:
                    return user
            return False
        except Exception as e:
            return e

    def get_call_by_id(self, call_id: str) -> dict:
        url = f"{self.__base_url}/v1/calls/{call_id}"
        try:
            response = requests.get(url)
            return response.json()
        except Exception as e:
            return e

    def transfer_call(self, call_id, user_id):
        url = f"{self.__base_url}/v1/calls/{call_id}/transfers"
        data = {"user_id": user_id}
        try:
            requests.post(url, data=data)
        except Exception as e:
            return e
