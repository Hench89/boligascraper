from os import path, listdir
import json
import zlib
import pandas as pd
import numpy as np
import datetime

def load_json_file(file_path):
    with open(file_path, "rb") as f:
        bytes = f.read()
    decompressed_data = zlib.decompress(bytes)
    decoded_data = decompressed_data.decode('utf-8')
    json_dict = json.loads(decoded_data)
    return json_dict

def load_json_folder(folder_path):

    files = listdir(folder_path)
    if len(files)==0:
        return None

    dict_list = []
    for f in files:
        try:
            file_path = f'{folder_path}/{f}'
            json_dict = load_json_file(file_path)
            dict_list.append(json_dict)
        except:
            print(f'error with file: {f}')

    return dict_list

def get_latest_file(folder_path):
    files = listdir(folder_path)
    if len(files)==0:
        return None
    files.sort(reverse=True)
    return f'{folder_path}/{files[0]}'

def add_days_ago(df, from_col, column_name):
    now_days = pd.to_datetime(datetime.datetime.now())
    created_days = pd.to_datetime(df[from_col], format='%Y-%m-%dT%H:%M:%S.%fZ')
    time_delta = now_days - created_days
    time_delta_as_days = round(time_delta / np.timedelta64(1, "D"))
    df[column_name] = time_delta_as_days.astype(int)
    return df