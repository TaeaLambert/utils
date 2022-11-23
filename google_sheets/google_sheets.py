import os
import gspread
import pandas as pd
from pathlib import Path


def google_crential_env_to_file():
    with open(os.getenv("GOOGLE_CONFIG_LOCATION"), "w") as f:
        f.write(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))


class google_sheets:
    __client: gspread.Client

    def __init__(self):
        my_file = Path(os.getenv("GOOGLE_CONFIG_LOCATION"))
        if my_file.is_file():
            self.__client = gspread.service_account(os.getenv("GOOGLE_CONFIG_LOCATION"))
        else:
            google_crential_env_to_file()
            self.__client = gspread.service_account(os.getenv("GOOGLE_CONFIG_LOCATION"))

    # def download_google_sheet(self, spreadsheetId):
    #     access_token = self.__client.auth.token
    #     url = (
    #         "https://www.googleapis.com/drive/v3/files/"
    #         + spreadsheetId
    #         + "/export?mimeType=application%2Fvnd.openxmlformats-officedocument.spreadsheetml.sheet"
    #     )
    #     res = requests.get(url, headers={"Authorization": "Bearer " + access_token})
    #     book = openpyxl.load_workbook(filename=BytesIO(res.content), data_only=False)
    #     return book

    def download_google_sheet(self, sheet_id, worksheet):
        sh = self.__client.open_by_key(sheet_id)
        worksheet = sh.worksheet(worksheet)
        return pd.DataFrame(worksheet.get_all_records())

    def set_cell_state(self, sheet_id, worksheet, cell, value):
        sh = self.__client.open_by_key(sheet_id)
        worksheet = sh.worksheet(worksheet).update_acell(cell, value)
        return f"{worksheet} cell: {cell} set to {value}"
