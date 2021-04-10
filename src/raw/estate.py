import json
from .utils import (
    compress_save, 
    decompresse_load, 
    compare_number_sets, 
    read_json_from_url,
    get_latest_file
)
from os import listdir, path
import pandas as pd


def extract_estate(list_path, estate_path, fetch_type, zipcodes = []):

    if len(zipcodes)==0:
        return print('.. zipcodes not configured correctly!')

    estate_ids = estate_ids = read_estate_ids(estate_path)
    list_ids = read_list_ids(list_path, fetch_type, zipcodes)

    # determine which archive ids are missing
    missing_ids, already_got_ids, only_archive_ids = compare_number_sets(list_ids, estate_ids)
    print(f'found {len(missing_ids)} missing ids')
    print(f'found {len(already_got_ids)} ids already in archive')
    print(f'found {len(only_archive_ids)} ids only in archive')

    # fetch missing estates to archive
    fetch_estates(estate_path, missing_ids, fetch_type)


def fetch_estates(estate_path, ids, fetch_type):

    def get_estate_url(estate_id):
        return f'https://api.boliga.dk/api/v2/estate/{estate_id}'

    for i, id in enumerate(ids):
        if id == 0:
            continue
        url = get_estate_url(id)
        print(f'Fetching {fetch_type} data for id {id} ({i+1} of {len(ids)})')
        data = read_json_from_url(url)
        data_str = json.dumps(data)

        file_path = f'{estate_path}/{id}.zlib'
        compress_save(file_path, data_str)


def read_estate_ids(folder_path):

    if not path.exists(folder_path):
        return []

    files = listdir(folder_path)
    split_files = [path.splitext(f)[0] for f in files]
    return [int(f) for f in split_files]


def read_list_ids(list_path, fetch_type, zipcodes):

    # if no folder
    if not path.exists(list_path):
        return []

    # if no file
    file_path = get_latest_file(list_path)
    if file_path is None:
        return []

    # load data as dataframe and filter on zipcodes
    data = decompresse_load(file_path)
    json_data = json.loads(data)
    df = pd.DataFrame(json_data)
    df = df[df['zipCode'].isin(zipcodes)]

    # return ids
    id_column = 'estateId' if fetch_type == 'sold' else 'id'
    estate_ids = df[id_column]
    return estate_ids
