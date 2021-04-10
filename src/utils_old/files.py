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


