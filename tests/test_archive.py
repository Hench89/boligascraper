from agent import archive
from agent.utils import create_dirs_for_file
import os


test_data = [{'estate_id' : 1, 'price': 100000}, {'estate_id' : 2, 'price': 100000}]


def test_save_dict():
    file_path = 'tests/generated/test_data.json'
    create_dirs_for_file(file_path)
    archive.save_dict(test_data, file_path)
    assert os.path.exists(file_path)


def test_load_dict():
    file_path = 'tests/generated/test_data.json'
    data = archive.load_dict(file_path)
    assert data == test_data


def test_load_dataframe_from_file():
    file_path = 'tests/generated/test_data.json'
    create_dirs_for_file(file_path)
    archive.save_dict(test_data, file_path)
    df = archive.load_dataframe_from_file(file_path)
    assert df.shape == (2, 2)


def test_read_ids_dict():
    file_path = 'tests/generated/test_data.json'
    create_dirs_for_file(file_path)
    archive.save_dict(test_data, file_path)
    estate_ids = archive.read_ids_from_list_file(file_path)
    assert estate_ids == set([1, 2])
