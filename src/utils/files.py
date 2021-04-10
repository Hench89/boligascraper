import requests as r
import zlib
import json
from os import path, makedirs

def dict_to_json(dict, file_path):
    output = json.dumps(dict)
    with open(file_path, 'w') as f:
        f.write(output)


def read_json_from_url(url):
    return r.get(url).json()


def read_local_json(file_path):
    with open(file_path) as f:
        return json.load(f)


def save_json_file(file_path, data):
    with open(file_path, 'w') as outfile:
        json.dump(data, outfile)


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
