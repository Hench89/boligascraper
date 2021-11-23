import json, gzip, os
from .utils import create_dirs_for_file


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


def read_ids_from_list_file(file_path: str):
    with gzip.open(file_path, 'rb') as f:
        file_content = f.read()
    json_data = json.loads(file_content)
    estate_ids = [x['estate_id'] for x in json_data]
    return set(estate_ids)


def load_all_dict_files_in_folder(dir_path: str) -> list:
    gz_files = read_all_gz_file_names(dir_path)
    dict_list = [load_dict(f) for f in gz_files]
    return dict_list


def identify_ids_already_downloaded(folder_path: str) -> list:
    gz_files = [f for f in os.listdir(folder_path) if f.endswith('.gz')]
    file_names = [os.path.splitext(f)[0] for f in gz_files]
    numeric_file_names = [int(f) for f in file_names if f.isnumeric()]
    return numeric_file_names


def identify_new_ids_to_download(list_ids, archive_ids) -> list:
    relevant_list_ids = set(list_ids)
    relevant_list_ids.remove(0)  # 0 when data only exist in list
    ids_only_in_list = relevant_list_ids.difference(archive_ids)
    return list(ids_only_in_list)
