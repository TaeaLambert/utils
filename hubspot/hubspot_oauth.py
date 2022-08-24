import os
from datetime import datetime, timedelta

import program.utils.hubspot.hubspot_api as hubspot_api
from program.utils.hubspot.mongodb import get_tokens_by_portal_id_mongodb, save_token_mongodb
from program.utils.hubspot.files import write_to_json_overwite

# 1st to run
def hubspot_login(code: str) -> list[str]:
    """_summary_
    This funtion is used to call other funtions to install the application into a hubspot portal

    Args:
        code (str): This is a code provided by hubspot in the url

    Returns:
        list[str]: A portal id so the program can redirect correctly
    """
    print("login")
    tokens = oauth_login(code)
    if tokens:
        print("saving tokens.....")
        hub = check_access_token(tokens["access_token"])
        tokens["portal_id"] = str(hub["hub_id"])
        save_token_mongodb(tokens)
        print("saved tokens.....")
        return str(hub["hub_id"])
    return 400


# 2nd to run V1
def oauth_login(code: str) -> dict or None:
    """_summary_
    This funtion is used when the hubspot application is installed into a portal

    Args:
        code (str): This is a code provided by hubspot in the url

    Returns:
        dict or None: _description_
    """
    print(os.getenv("REDIRECT_URI"))
    url = "https://api.hubapi.com/oauth/v1/token"
    formData = (
        f"grant_type=authorization_code&code={code}"
        + "&redirect_uri="
        + os.getenv("REDIRECT_URI")
        + "&client_id="
        + os.getenv("CLIENT_ID")
        + "&client_secret="
        + os.getenv("CLIENT_SECRET")
    )
    response = hubspot_api.token_api_request(url, "POST", data=formData)
    if response.status_code != 400:
        return response.data
    else:
        return None


# 2nd to run V2
def hubspot_login_create_properties(code: str) -> list[str, str]:
    """_summary_
    This funtion is used when the hubspot application is installed into a portal
    and the program must create a one or more properties before the login process is completed.

    Args:
        code (str):  This is a code provided by hubspot in the url

    Returns:
        list[str, str]: the access token that will be used to create the properties and a portal id so the program can redirect correctly.
    """
    print("login")
    tokens = oauth_login(code)
    if tokens:
        print("saving tokens.....")
        hub = check_access_token(tokens["access_token"])
        tokens["portal_id"] = str(hub["hub_id"])
        save_token_mongodb(tokens)
        print("saved tokens.....")
        return [tokens["access_token"], str(hub["hub_id"])]
    return 400


# 3rd to run
def check_access_token(access_token: str) -> dict or False:
    """_summary_
    This funtion is used to get the hubspot portal id where the application was installed into

    Args:
        access_token (str): The bearer token that will be sent to hubspot rest api

    Returns:
        dict or False: dict of all the data returned by the request. If the the request returns a error False will be returned
    """
    url = "https://api.hubapi.com/oauth/v1/access-tokens/" + access_token
    response = hubspot_api.token_api_request(url, "GET")
    if response.status_code == 200:
        return response.data
    else:
        return False


def get_access_token(portal_id: int) -> str or False:
    """_summary_
    This funtion gets a new refreshed access token from hubspot for the application depending on the portal id
    first the tokens saved within the selected DB (.env file). The program selects the refesh token which
    is used to get a new access token from hubspot.

    Args:
        portal_id (int): The protal id that will be used to gather the refresh token.

    Returns:
        str or False: If the request is successfully completed the a access token will be returned else False will be returned.
    """
    tokens = get_tokens_by_portal_id_mongodb(portal_id)
    refresh_token = tokens["refresh_token"]
    formData = (
        "grant_type=refresh_token&client_id="
        + os.getenv("CLIENT_ID")
        + "&client_secret="
        + os.getenv("CLIENT_SECRET")
        + "&redirect_uri="
        + os.getenv("REDIRECT_URI")
        + "&refresh_token="
        + refresh_token
    )
    url = "https://api.hubapi.com/oauth/v1/token"
    try:
        new_tokens = hubspot_api.token_api_request(url, "POST", data=formData).data
        date_time_plus_25_minutes = datetime.now() + timedelta(minutes=25)
        tokens_for_save = {
            "access_token": new_tokens["access_token"],
            "expires_at": date_time_plus_25_minutes.isoformat(),
        }
        write_to_json_overwite(tokens_for_save, f"./tokens/tokens_{portal_id}.json")
    except Exception as e:
        print(e)
        return False
    return new_tokens["access_token"]
