from os import listdir
import json
import zlib


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
