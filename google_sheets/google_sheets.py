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

    def set_cell_format(self, sheet_id, worksheet, cell, value):
        """_summary_

        Args:
            sheet_id (_type_): _description_
            worksheet (_type_): _description_
            cell (_type_): _description_
            value (_type_): _description_

            {
                "backgroundColor": {
                "red": 0.0,
                "green": 0.0,
                "blue": 0.0
                },
                "horizontalAlignment": "CENTER",
                "textFormat": {
                "foregroundColor": {
                    "red": 1.0,
                    "green": 1.0,
                    "blue": 1.0
                },
                "fontSize": 12,
                "bold": True
                }
            }

        Returns:
            _type_: _description_
        """
        sh = self.__client.open_by_key(sheet_id)
        worksheet = sh.worksheet(worksheet).format(cell, value)
        return f"{worksheet} cell: {cell} formatted to {value}"
