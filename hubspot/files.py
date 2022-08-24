import pathlib as Path
import json


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
