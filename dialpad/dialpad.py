import requests


class Dialpad_client:
    __header: str = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer ",
    }

    def __init__(self, access_token) -> None:
        self.__header["Authorization"] = "Bearer " + access_token

    def get_dialpad_user_by_email(self, email: str) -> dict:
        url = f"https://dialpad.com/api/v2/users?email={email}"
        try:
            response = requests.get(url, headers=self.__header)
            return response.json()
        except Exception as e:
            return e

    def get_call_by_id(self, call_id: str) -> dict:
        url = f"https://dialpad.com/api/v2/call/{call_id}"
        try:
            response = requests.get(url, headers=self.__header)
            return response.json()
        except Exception as e:
            return e

    def transfer_call(self, call_id, phone_to_transfer_to):
        url = f"https://dialpad.com/api/v2/call/{call_id}/transfer"
        payload = {"transfer_to_number": phone_to_transfer_to, "custom_data": "Transferred call"}

        try:
            return requests.post(url, json=payload, headers=self.__header).json()
        except Exception as e:
            return e
