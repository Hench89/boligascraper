from archive import Archive
from typing import List, Set
from schema import ListItem, Estate
import json, gzip, os


class FolderArchive(Archive):

    def save_list_result(self, data: List[ListItem], save_path: str) -> None:
        list_of_dict = [li.as_dict for li in data]
        _save_json(list_of_dict, save_path)


    def read_list_result(self, read_path: str) -> List[ListItem]:
        print('reading', read_path)
        with gzip.open(read_path, 'rb') as f:
            file_content = f.read()
        json_deserialized = json.loads(file_content)
        list_result = [ListItem(**d) for d in json_deserialized]
        return list_result


    def save_estate_collection(self, data: List[Estate], save_path: str) -> None:
        list_of_dict = [li.as_dict for li in data]
        _save_json(list_of_dict, save_path)


    def read_estate_collection(self, read_path: str) -> List[Estate]:
        with gzip.open(read_path, 'rb') as f:
            file_content = f.read()
        json_deserialized = json.loads(file_content)
        list_result = [Estate(**d) for d in json_deserialized]
        return list_result


    def identify_missing_and_removed_ids(self, )


def _save_json(data, save_path):
    _create_dirs(save_path)
    json_serialized = json.dumps(data).encode('utf-8')
    with gzip.open(save_path, 'wb') as f:
        f.write(json_serialized)



def _create_dirs(file_path: str):
    abs_file_path = os.path.abspath(file_path)
    dir_name = os.path.dirname(abs_file_path)
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
