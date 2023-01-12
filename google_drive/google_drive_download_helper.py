import os
import settings
import requests
from pathlib import Path
from oauth2client.service_account import ServiceAccountCredentials
from program.utils.google_drive.enums import googleDriveFileExportType, googleDriveFileType


class google_drive_download_helper:
    """_summary_

    https://spreadsheet.dev/comprehensive-guide-export-google-sheets-to-pdf-excel-csv-apps-script
    """

    def __init__(self, location_to_service_account: Path = None):
        self.scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        if location_to_service_account != None:
            self.__cred = ServiceAccountCredentials.from_json_keyfile_name(location_to_service_account, self.scope)
        else:
            self.__cred = ServiceAccountCredentials.from_json_keyfile_name(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"), self.scope)
        self.__headers = {"Authorization": "Bearer " + self.__cred.create_delegated("").get_access_token().access_token}

    def download_file(
        self,
        file_download_location: Path,
        file_id: str,
        file_type: googleDriveFileType,
        file_export_type: googleDriveFileExportType,
        extra_format_options: str = None,
    ) -> requests.Response:

        url = f"https://docs.google.com/{file_type.value}/export?id={file_id}&format={file_export_type.value}"
        url += extra_format_options if extra_format_options != None else url
        res: requests.Response = requests.get(url, headers=self.__headers)
        res.raise_for_status()
        with open(file_download_location, "wb") as f:
            f.write(res.content)
        return res
