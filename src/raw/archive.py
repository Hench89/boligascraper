from os import path, makedirs, listdir
import requests
import zlib
import json
from datetime import datetime
import time
import pandas as pd


def load_latest_batch_from_archive(folder_path):
    try:
        files = listdir(folder_path)
        files.sort(reverse=True)
        return f'{folder_path}/{files[0]}'
    except Exception:
        return None


def read_estate_ids(folder_path):
    if not path.exists(folder_path):
        return []
    files_in_folder = listdir(folder_path)
    split_files = [path.splitext(f)[0] for f in files_in_folder]
    return [int(f) for f in split_files]


def get_file_age_hours(file_path):
    age_seconds = time.time() - path.getmtime(file_path)
    age_minutes = int(age_seconds) / 60
    age_hours = round(age_minutes / 60)
    return age_hours


def save_list_data(data, folder_path: str):
    f = create_datetime_file_path(folder_path)
    if type(data) == list:
        data = json.dumps(data)
    data = encode(data)
    data = compress(data)
    write_bytes(f, data)


def create_datetime_file_path(folder_path: str):
    time_str = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    file_path = f'{folder_path}/{time_str}.zlib'
    return file_path


def encode(data):
    return bytes(data, encoding='utf-8')


def compress(data):
    return zlib.compress(data)


def write_bytes(file_path: str, data):
    dir_name = path.dirname(file_path)
    if not path.exists(dir_name):
        makedirs(dir_name)
    with open(file_path, "wb") as f:
        f.write(data)


def read_json_data(file_path):
    x = read_bytes(file_path)
    x = decompress(x)
    x = decode(x)
    x = json.loads(x)
    return x


def read_bytes(file_path: str):
    with open(file_path, "rb") as f:
        bytes = f.read()
    return bytes


def decompress(bytes):
    return zlib.decompress(bytes)


def decode(data):
    return data.decode('utf-8')


def read_ids_from_list_data(list_path, zipcodes, id_column):
    if not path.exists(list_path):
        return []
    file_path = load_latest_batch_from_archive(list_path)
    if file_path is None:
        return []

    data = read_json_data(file_path)
    print(data)
    df = pd.DataFrame(data)
    df = df[df['zipCode'].isin(zipcodes)]
    estate_ids = df[id_column]
    return estate_ids
