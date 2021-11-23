import json, gzip, os
from .utils import create_dirs_for_file
import pandas as pd


def save_dict(data, file_path: str):
    create_dirs_for_file(file_path)
    data = json.dumps(data).encode('utf-8')
    with gzip.open(file_path, 'wb') as f:
        f.write(data)


def load_dict(file_path: str):
    with gzip.open(file_path, 'rb') as f:
        file_content = f.read()
    json_data = json.loads(file_content)
    return json_data


def load_dataframe_from_file(file_path: str):
    d = load_dict(file_path)
    df = pd.DataFrame(d)
    return df


def load_dataframe_from_dir(dir_path: str):
    files = read_files_with_numeric_name(dir_path)
    dict_list = [load_dict(f'{dir_path}/{f}') for f in files]
    df = pd.DataFrame(dict_list)
    return df


def read_ids_from_list_file(file_path: str):
    with gzip.open(file_path, 'rb') as f:
        file_content = f.read()
    json_data = json.loads(file_content)
    estate_ids = [x['estate_id'] for x in json_data]
    return set(estate_ids)


def identify_ids_already_downloaded(dir_path: str) -> list:
    files = read_files_with_numeric_name(dir_path)
    files_wo_extension = [os.path.splitext(f)[0].isnumeric() for f in files]
    files_as_int = [int(f) for f in files_wo_extension]
    return files_as_int


def identify_new_ids_to_download(list_ids, archive_ids) -> list:
    relevant_list_ids = set(list_ids)
    relevant_list_ids.remove(0)  # 0 when data only exist in list
    ids_only_in_list = relevant_list_ids.difference(archive_ids)
    return list(ids_only_in_list)


def read_files_with_numeric_name(dir_path: str):
    files = [f for f in os.listdir(dir_path)]
    numeric_files = [f for f in files if os.path.splitext(f)[0].isnumeric()]
    return numeric_files
