from os import path, makedirs, listdir
import requests
import zlib
from json import dumps
from datetime import datetime

def load_latest_batch_from_archive(folder_path):
    try:
        files = listdir(folder_path)
        files.sort(reverse=True)
        return f'{folder_path}/{files[0]}'
    except Exception:
        return None


def get_file_age_hours(file_path):
    try:
        age_seconds = time.time() - path.getmtime(file_path)
        age_minutes = int(age_seconds) / 60
        age_hours = round(age_minutes / 60)
        return age_hours
    except Exception:
        return None


def compress_json_and_save_list(file_path, data):
    if type(data) == list:
        data = dumps(data)

    dir_name = path.dirname(file_path)
    if not path.exists(dir_name):
        makedirs(dir_name)

    encoded_data = bytes(data, encoding='utf-8')
    compressed_data = zlib.compress(encoded_data)
    with open(file_path, "wb") as f:
        f.write(compressed_data)


def create_datetime_file_path(folder_path: str):
    time_str = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    file_path = f'{folder_path}/{time_str}.zlib'
    return file_path
