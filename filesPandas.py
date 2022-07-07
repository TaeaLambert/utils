import pandas as pd


def json_to_csv(json_path, csv_path):
    df = pd.read_json(json_path)
    df.to_csv(csv_path, index=False)
