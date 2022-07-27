import json
import csv
import pathlib as Path
import pandas as pd


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


def json_to_csv(json_path, csv_path):
    df = pd.read_json(json_path)
    df.to_csv(csv_path, index=False)


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
