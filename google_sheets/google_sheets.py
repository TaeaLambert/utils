import gspread
import settings
import pandas as pd


class google_sheets:
    __client: gspread.Client

    def __init__(self):
        self.__client = settings.gc

    def download_google_sheet(self, sheet_id, worksheet):
        sh = self.__client.open_by_key(sheet_id)
        worksheet = sh.worksheet(worksheet)
        return pd.DataFrame(worksheet.get_all_records())

    def set_cell_state(self, sheet_id, worksheet, cell, value):
        sh = self.__client.open_by_key(sheet_id)
        worksheet = sh.worksheet(worksheet).update_acell(cell, value)
        return f"{worksheet} cell: {cell} set to {value}"
