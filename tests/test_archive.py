from agent import archive
from agent.utils import create_dirs_for_file
import os
import pytest


file_data = [
    [{'estate_id' : 1, 'price': 100000}, {'estate_id' : 2, 'price': 100000}],
    [{'estate_id' : 3, 'price': 100000}, {'estate_id' : 4, 'price': 100000}]
]
paths = [
    'tests/generated/archive/data01.json',
    'tests/generated/archive/data02.json'
]
dir_path = 'tests/generated/archive/'


@pytest.fixture(scope='module')
def file_setup():
    for d, p in zip(file_data, paths):
        create_dirs_for_file(p)
        archive.save_dict(d, p)


def test_that_file_was_created(file_setup):
    assert os.path.exists(paths[0])


def test_that_loaded_file_equals_data_saved(file_setup):
    assert archive.load_dict(paths[0]) == file_data[0]


def test_that_dataframe_can_be_loaded_from_file(file_setup):
    df = archive.load_dataframe_from_file(paths[0])
    assert df.shape == (2, 2)


def test_that_ids_can_be_read_from_file(file_setup):
    estate_ids = archive.read_ids_from_list_file(paths[0])
    assert estate_ids == set([1, 2])


def test_that_dataframe_can_be_loaded_from_dir(file_setup):
    df = archive.load_dataframe_from_dir(dir_path)
    assert df.shape == (4, 2)