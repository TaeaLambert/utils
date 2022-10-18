import os
import settings
from google.cloud.firestore_v1 import Client


class Firestore_Client:
    __client: Client

    def __init__(self) -> None:
        self.__client = settings.get_firestore_client().collection(os.getenv("COLLECTION") + "-data")

    def increment_code_firestore(self, portal_id, object_type, property, increment_value, value_to_start_at):
        values_in_db: dict = self.__client.document(portal_id).get().exists
        if object_type in values_in_db:
            if property in values_in_db[object_type]:
                values_in_db[object_type][property] = values_in_db[object_type][property] + increment_value
                return values_in_db[object_type][property]
            else:
                values_in_db[object_type][property] = value_to_start_at
                return value_to_start_at
        else:
            values_in_db[object_type] = {property: value_to_start_at}
            self.__client.document(portal_id).set(values_in_db)
            return value_to_start_at

    def get_code_firestore(self, portal_id, object_type, property):
        values_in_db: dict = self.__client.document(portal_id).get().exists
        if object_type in values_in_db:
            if property in values_in_db[object_type]:
                return values_in_db[object_type][property]
            else:
                return None
        else:
            return None

    def reset_code_firestore(self, portal_id, object_type, property):
        values_in_db: dict = self.__client.document(portal_id).get().exists
        if object_type in values_in_db:
            if property in values_in_db[object_type]:
                True
            else:
                return None
        else:
            return None
