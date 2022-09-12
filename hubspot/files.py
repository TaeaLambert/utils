import pathlib as Path
import json
import glob
import os


def write_to_json_overwite(data: dict or list, path: Path):
    """_summary_
    This funtions writes the passed in data into a .json file detirmaned by the path passed in

    Args:
        data (dictorlist): Data that is writen into file
        path (Path): path to the file that data will be saved into

    """
    # write data to a json file
    with open(path, "w", encoding="utf8") as outfile:
        json.dump(data, outfile)


def json_to_dict(path: Path):
    """_summary_
    Opens a .json file that is determined by the path veriable that is passed in
    and converts the data within into a dict veriable that is passed back to the
    funtions caller

    Args:
        path (Path): Path to the .json file

    Returns:
        dict: Contains all the data within the .json file
    """
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_to_file(data, path):
    # write data to a json file
    with open(path, "w", encoding="utf8") as outfile:
        outfile.write(data)
    return "done"


def get_lastest_file(path):
    list_of_files = glob.glob(path)  # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    print(latest_file)
    return latest_file
