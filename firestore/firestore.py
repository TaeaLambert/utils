import os
import settings
from google.cloud.firestore_v1 import Client, DocumentSnapshot


class Firestore_Client:
    __client: Client

    def __init__(self) -> None:
        self.__client = settings.get_firestore_client().collection(os.getenv("COLLECTION") + "-data")

    def increment_code_firestore(self, portal_id, object_type, property, increment_value, value_to_start_at):
        if self.__client.document(portal_id).get().exists == False:
            values_in_db = {object_type: {property: value_to_start_at}}
            self.__client.document(portal_id).set(values_in_db)
            return value_to_start_at
        else:
            values_in_db: DocumentSnapshot = self.__client.document(portal_id).get().to_dict()
            if object_type in values_in_db:
                if property in values_in_db[object_type]:
                    values_in_db[object_type][property] = values_in_db[object_type][property] + increment_value
                    self.__client.document(portal_id).set(values_in_db)
                    return values_in_db[object_type][property]
                else:
                    values_in_db[object_type][property] = value_to_start_at
                    return value_to_start_at
            else:
                values_in_db = {object_type: {property: value_to_start_at}}
                self.__client.document(portal_id).set(values_in_db)
                return value_to_start_at

    def reset_code_firestore(self, portal_id, object_type, property, value):
        if self.__client.document(portal_id).get().exists == True:
            values_in_db = self.__client.document(portal_id).get().to_dict()
            if object_type in values_in_db:
                if property in values_in_db[object_type]:
                    if value == "Nothing":
                        values_in_db[object_type].pop(property)
                        self.__client.document(portal_id).set(values_in_db)
                    else:
                        values_in_db[object_type][property] = value
                        self.__client.document(portal_id).set(values_in_db)
                    return True
                else:
                    return None
            else:
                return None
        else:
            return None
