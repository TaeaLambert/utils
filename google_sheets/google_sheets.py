import json
import gspread
import settings
import pandas as pd
from typing import Literal


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

    def set_csv_into_sheet(
        self,
        sheet_name: str,
        worksheet: str,
        csv_data: list,
        cell: str = "A1",
        sort: bool = False,
        sort_column: int = 1,
        sort_type: Literal["asc", "des"] = "asc",
        sort_range: str = "A1:Q50000",
    ):
        try:
            sh = self.__client.open(sheet_name).worksheet(worksheet)
            sh.clear()
            sh.update(cell, csv_data)
            if sort != False:
                sh.sort((sort_column, sort_type), range=sort_range)
            return True
        except Exception as e:
            raise e
