import os
import datetime

from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.files.file import File


class SharePoint:
    def __init__(self, sharepoint_site, sharepoint_site_name, sharepoint_doc) -> None:
        self.sharepoint_site = sharepoint_site
        self.sharepoint_site_name = sharepoint_site_name
        self.sharepoint_doc = sharepoint_doc

    def _auth(self):
        conn = ClientContext(self.sharepoint_site).with_credentials(
            ClientCredential(os.getenv("SHAREPOINT_CLIENT_ID"), os.getenv("SHAREPOINT_CLIENT_SECRET"))
            # UserCredential(os.getenv("USERNAME"), os.getenv("PASSWORD"))
        )
        return conn

    def create_sharepoint_directory(self, dir_name: str):
        """
        Creates a folder in the sharepoint directory.
        """
        if dir_name:
            ctx = self._auth()
            result = ctx.web.folders.add(f"{self.sharepoint_doc}/{dir_name}").execute_query()
            if result:
                # documents is titled as Shared Documents for relative URL in SP
                relative_url = f"{self.sharepoint_doc}/{dir_name}"
                return relative_url

    def _get_files_list(self, folder_name):
        conn = self._auth()
        target_folder_url = f"{self.sharepoint_doc}/{folder_name}"
        root_folder = conn.web.get_folder_by_server_relative_url(target_folder_url)
        root_folder.expand(["Files", "Folders"]).get().execute_query()
        return root_folder.files

    def download_file(self, file_name, folder_name):
        conn = self._auth()
        file_url = f"/sites/{self.sharepoint_site_name}/{self.sharepoint_doc}/{folder_name}/{file_name}"
        file = File.open_binary(conn, file_url)
        return file.content

    def download_latest_file(self, folder_name):
        date_format = "%Y-%m-%dT%H:%M:%SZ"
        files_list = self._get_files_list(folder_name)
        file_dict = {}
        for file in files_list:
            dt_obj = datetime.datetime.strptime(file.time_last_modified, date_format)
            file_dict[file.name] = dt_obj
        # sort dict object to get the latest file
        file_dict_sorted = {key: value for key, value in sorted(file_dict.items(), key=lambda item: item[1], reverse=True)}
        latest_file_name = next(iter(file_dict_sorted))
        content = self.download_file(latest_file_name, folder_name)
        return latest_file_name, content

    def upload_file(self, file_name, folder_name, content):
        conn = self._auth()
        target_folder_url = f"/sites/{self.sharepoint_site_name}/{self.sharepoint_doc}/{folder_name}"
        if target_folder_url[len(target_folder_url) - 1 : len(target_folder_url)] == "/":
            target_folder_url = target_folder_url[:-1]
        target_folder = conn.web.get_folder_by_server_relative_path(target_folder_url)
        try:
            response = target_folder.upload_file(file_name, content).execute_query()
        except Exception as e:
            print(e)
            return e
        return response

    def upload_file_in_chunks(self, file_path, folder_name, chunk_size, chunk_uploaded=None, **kwargs):
        conn = self._auth()
        target_folder_url = f"/sites/{self.sharepoint_site_name}/{self.sharepoint_doc}/{folder_name}"
        target_folder = conn.web.get_folder_by_server_relative_path(target_folder_url)
        response = target_folder.files.create_upload_session(
            source_path=file_path, chunk_size=chunk_size, chunk_uploaded=chunk_uploaded, **kwargs
        ).execute_query()
        return response

    def get_list(self, list_name):
        conn = self._auth()
        target_list = conn.web.lists.get_by_title(list_name)
        items = target_list.items.get().execute_query()
        return items

    def get_file_properties_from_folder(self, folder_name):
        files_list = self._get_files_list(folder_name)
        properties_list = []
        for file in files_list:
            file_dict = {
                "file_id": file.unique_id,
                "file_name": file.name,
                "major_version": file.major_version,
                "minor_version": file.minor_version,
                "file_size": file.length,
                "time_created": file.time_created,
                "time_last_modified": file.time_last_modified,
            }
            properties_list.append(file_dict)
            file_dict = {}
        return properties_list
