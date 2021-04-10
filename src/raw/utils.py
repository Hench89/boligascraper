import requests as r
import json
from os import path, makedirs, listdir
import zlib
import time


def read_json_from_url(url):
    return r.get(url).json()


def compress_save(file_path, data):

    # create dirs if missing
    dir_name = path.dirname(file_path)
    if not path.exists(dir_name):
        makedirs(dir_name)

    # encode and compress
    encoded_data = bytes(data, encoding='utf-8')    
    compressed_data = zlib.compress(encoded_data)

    # save file
    with open(file_path, "wb") as f:
        f.write(compressed_data)


def decompresse_load(file_path):
    with open(file_path, "rb") as f:
        bytes = f.read()
    decompressed_data = zlib.decompress(bytes)
    decoded_data = decompressed_data.decode('utf-8')
    return decoded_data


def compare_number_sets(list_a, list_b):

    if list_a is None or list_b is None:
        return list_a or [], list_b or []

    # cast as sets
    seta = set(list_a)
    setb = set(list_b)

    # find differences
    a_set_only = seta.difference(setb)
    set_intersection = setb.intersection(seta)
    b_set_only = setb.difference(seta)

    return list(a_set_only), list(set_intersection), list(b_set_only)


def get_latest_file(folder_path):

    if not path.exists(folder_path):
        return None

    files = listdir(folder_path)
    if len(files)==0:
        return None
    files.sort(reverse=True)
    return f'{folder_path}/{files[0]}'


def get_latest_file_data(folder_path):
    latest_file = get_latest_file(folder_path)
    data = decompresse_load(latest_file)
    return json.loads(data)


def file_age_hours(file_path):
    age_seconds = time.time() - path.getmtime(file_path)
    age_minutes = int(age_seconds) / 60
    age_hours = age_minutes / 60
    return round(age_hours)
