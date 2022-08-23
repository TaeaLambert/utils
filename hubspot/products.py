from datetime import datetime
from program.utils.files import csv_to_list, json_to_csv, write_to_json


def create_csv_and_convert_to_list(JSON_FILE, CSV_FILE, data):
    write_to_json(data, JSON_FILE)
    json_to_csv(JSON_FILE, CSV_FILE)
    del data
    list = csv_to_list(CSV_FILE)
    return list


def format_products(products: list[dict]):
    new_list = []
    object_holder = {}
    for result in products.get("results"):

        # Object Id
        object_holder["Object Id"] = result["id"]
        # Price AUD
        object_holder["Price AUD"] = result["properties"]["hs_price_aud"]
        # Price EUR
        object_holder["Price EUR"] = result["properties"]["hs_price_eur"]
        # Price NZD
        object_holder["Price NZD"] = result["properties"]["hs_price_nzd"]
        # Price USD
        object_holder["Price USD"] = result["properties"]["hs_price_usd"]
        # Unit price
        object_holder["Unit price"] = result["properties"]["price"]
        # Create Date
        new_createdAt = datetime.strptime(result["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ")
        object_holder["Create Date"] = new_createdAt.strftime("%Y-%m-%d %H:%M:%S")
        # Exclusions
        object_holder["Exclusions"] = result["properties"]["exclusions"]
        # Last Modified Date
        new_updatedAt = datetime.strptime(result["updatedAt"], "%Y-%m-%dT%H:%M:%S.%fZ")
        object_holder["Last Modified Date"] = new_updatedAt.strftime("%Y-%m-%d %H:%M:%S")
        # Name
        object_holder["Name"] = result["properties"]["name"]
        # Object ID
        object_holder["Object ID"] = result["id"]
        # Product Points
        object_holder["Product Points"] = result["properties"]["product_points"]
        # Product description
        object_holder["Product description"] = result["properties"]["description"]
        # Product image link
        object_holder["Product image link"] = result["properties"]["product_image_link"]
        # Resource Type
        object_holder["Resource Type"] = result["properties"]["product_type"]
        # Scope of Service
        object_holder["Scope of Service"] = result["properties"]["scope_of_service"]
        # URL
        object_holder["URL"] = result["properties"]["hs_url"]

        new_list.append(object_holder)
        object_holder = {}
    return new_list
