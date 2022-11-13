import os
import settings
from google.cloud.firestore_v1 import Client, DocumentSnapshot
from google.cloud.firestore_v1.transaction import Transaction
import google.cloud.firestore as firestore
from datetime import datetime, timedelta


class Firestore_Client:
    __client: Client

    def __init__(self) -> None:
        self.__client = settings.get_firestore_client().collection(os.getenv("COLLECTION") + "-data")

    # Increment code micro app

    def increment_code_firestore(self, portal_id, object_type, property, increment_value, value_to_start_at):
        if self.__client.document(portal_id).get().exists == False:
            values_in_db = {object_type: {property: value_to_start_at, property + "_lock": None}}
            self.__client.document(portal_id).set(values_in_db)
            return value_to_start_at
        else:

            values_in_db: DocumentSnapshot = self.__client.document(portal_id).get().to_dict()
            if object_type in values_in_db:
                if property in values_in_db[object_type]:
                    if property + "_lock" in values_in_db[object_type]:
                        if values_in_db[object_type][property + "_lock"] != None and values_in_db[object_type][
                            property + "_lock"
                        ] < datetime.now() + timedelta(minutes=1):
                            return None

                        transaction = settings.get_firestore_client().transaction()
                        ref = self.__client.document(portal_id)
                        try:
                            return self.update_in_transaction_increment(
                                transaction,
                                ref,
                                object_type=object_type,
                                property=property,
                                increment=increment_value,
                            )
                        except Exception as e:
                            print(e)
                            raise e
                    else:
                        transaction = settings.get_firestore_client().transaction()
                        ref = self.__client.document(portal_id)
                        try:
                            return self.update_in_transaction_increment(
                                transaction,
                                ref,
                                object_type=object_type,
                                property=property,
                                increment=increment_value,
                            )
                        except Exception as e:
                            print(e)
                            raise e
                else:
                    values_in_db[object_type][property] = value_to_start_at
                    values_in_db[object_type][property + "_lock"] = None
                    self.__client.document(portal_id).set(values_in_db)
                    return value_to_start_at
            else:
                values_in_db = {object_type: {property: value_to_start_at, property + "_lock": None}}
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

    @firestore.transactional
    def update_in_transaction_increment(transaction: Transaction, ref: DocumentSnapshot, *args, **kwargs):
        snapshot: DocumentSnapshot = ref.get(transaction=transaction)
        snapshot_dict = snapshot.to_dict()

        snapshot_dict[kwargs["object_type"]][kwargs["property"] + "_lock"] = datetime.now()
        transaction.update(ref, snapshot_dict)

        snapshot_dict[kwargs["object_type"]][kwargs["property"]] = (
            snapshot_dict[kwargs["object_type"]][kwargs["property"]] + kwargs["increment"]
        )
        transaction.update(ref, snapshot_dict)

        snapshot_dict[kwargs["object_type"]][kwargs["property"] + "_lock"] = None
        transaction.update(ref, snapshot_dict)

        return snapshot_dict[kwargs["object_type"]][kwargs["property"]] + kwargs["increment"]

    # Generate unique code generator micro app

    def unique_num_letter_is_value_in_db(self, portal_id: str, object_type: str, property, value: str) -> bool or None:
        if self.__client.document(portal_id).get().exists == True:
            objects = self.__client.document(portal_id).get().to_dict()
            if object_type in objects:
                if property in objects[object_type]:
                    if value in objects[object_type][property]:
                        return True
                    else:
                        return False
                else:
                    return None
            else:
                return None
        else:
            return None

    def unique_num_letter_save_value_to_db(self, portal_id: str, object_type: str, property, value: str) -> bool or None:
        if self.unique_num_letter_is_value_in_db(portal_id, object_type, property, value) != True:

            value_1 = self.__client.document(portal_id).get()
            value_2 = self.__client.document(portal_id).get().exists

            if self.__client.document(portal_id).get().exists == True:
                objects = self.__client.document(portal_id).get().to_dict()
                if object_type in objects:
                    if property in objects[object_type]:
                        # self.update_in_transaction_unique_code_generator()
                        objects[object_type][property].append(value)
                        self.__client.document(portal_id).set(objects)
                    else:
                        objects[object_type][property] = [value]
                        self.__client.document(portal_id).set(objects)
                else:
                    objects[object_type] = {property: [value]}
                    self.__client.document(portal_id).set(objects)
            else:
                self.__client.document(portal_id).set({object_type: {property: [value]}})
        else:
            return False
        return True

    @firestore.transactional
    def update_in_transaction_unique_code_generator(transaction: Transaction, ref: DocumentSnapshot, *args, **kwargs):
        snapshot: DocumentSnapshot = ref.get(transaction=transaction)
        snapshot_dict = snapshot.to_dict()

        snapshot_dict[kwargs["object_type"]][kwargs["property"] + "_lock"] = datetime.now()
        transaction.update(ref, snapshot_dict)

        snapshot_dict[kwargs["object_type"]][kwargs["property"]] = (
            snapshot_dict[kwargs["object_type"]][kwargs["property"]] + kwargs["increment"]
        )
        transaction.update(ref, snapshot_dict)

        snapshot_dict[kwargs["object_type"]][kwargs["property"] + "_lock"] = None
        transaction.update(ref, snapshot_dict)

        return snapshot_dict[kwargs["object_type"]][kwargs["property"]] + kwargs["increment"]
