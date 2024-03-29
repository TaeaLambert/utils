import glob
import json
import csv
import os
import pathlib as Path


def write_to_json(data, path):
    # write data to a json file
    with open(path, "w", encoding="utf8") as outfile:
        json.dump(data, outfile)
    return "done"


def write_to_json_overwite(data, path):
    # write data to a json file
    with open(path, "w", encoding="utf8") as outfile:
        json.dump(data, outfile)
    return "done"


def write_to_txt(data, path):
    # write data to a json file
    with open(path, "w", encoding="utf8") as outfile:
        outfile.write(data)
    return "done"


def append_to_txt(data, path):
    # write data to a json file
    with open(path, "a", encoding="utf8") as outfile:
        outfile.write(data)
    return "done"


def csv_to_list(path: Path):
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        return list(reader)


def txt_to_list(path: Path):
    with open(path, encoding="utf-8") as f:
        return [line.strip().replace("\u200b", "") for line in f]


def json_to_dict(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_list_of_file_in_path(path: Path):
    return glob.glob(path)


def get_lastest_file(path):
    list_of_files = glob.glob(path)  # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    print(latest_file)
    return latest_file
