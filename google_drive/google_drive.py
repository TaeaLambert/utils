# from googleapiclient.discovery import build
# from googleapiclient.http import MediaIoBaseDownload
# from google.oauth2 import service_account

# import settings


# class google_drive:
#     # __client:str

#     def __init__(self):
#         self.__client = settings.Client


import os
import settings
import requests
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

cred = ServiceAccountCredentials.from_json_keyfile_name(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"), scope)

url = "https://docs.google.com/spreadsheets/export?format=zip&id=" + "1nuBta03d_TeOmlB9Eazpr0RJ3kkwuQkh"
headers = {"Authorization": "Bearer " + cred.create_delegated("").get_access_token().access_token}
res = requests.get(url, headers=headers)
with open("test.zip", "wb") as f:
    f.write(res.content)
