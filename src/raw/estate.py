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


def run(estate_archive_path, sold_archive_path = None, zipcodes = []):

    if len(zipcodes)==0:
        return print('.. zipcodes not configured correctly!')

    # fetch estate ids
    estate_ids = [] 
    if estate_archive_path:
        estate_ids = read_estate_ids(estate_archive_path)

    # fetch sold ids
    sold_ids = []
    if sold_archive_path:
        sold_ids = read_sold_ids(sold_archive_path, zipcodes)

    # determine which archive ids are missing
    missing_ids, already_got_ids, only_archive_ids = compare_number_sets(sold_ids, estate_ids)
    print(f'found {len(missing_ids)} missing ids')
    print(f'found {len(already_got_ids)} ids already in archive')
    print(f'found {len(only_archive_ids)} ids only in archive')

    # fetch missing estates to archive
    fetch_estates(estate_archive_path, missing_ids)


def fetch_estates(archive_path, ids):

    def get_estate_url(estate_id):
        return f'https://api.boliga.dk/api/v2/estate/{estate_id}'

    for i, id in enumerate(ids):
        if id == 0:
            continue
        url = get_estate_url(id)
        print(f'Processing id {id} ({i+1} of {len(ids)})')
        data = read_json_from_url(url)
        data_str = json.dumps(data)

        file_path = f'{archive_path}/{id}.zlib'
        compress_save(file_path, data_str)


def read_estate_ids(folder_path):

    if not path.exists(folder_path):
        return []

    files = listdir(folder_path)
    split_files = [path.splitext(f)[0] for f in files]
    return [int(f) for f in split_files]


def read_sold_ids(folder_path, zipcodes):

    # if no folder
    if not path.exists(folder_path):
        return []

    # if no file
    file_path = get_latest_file(folder_path)
    if file_path is None:
        return []

    # load data
    data = decompresse_load(file_path)
    json_data = json.loads(data)

    # filtering
    df = pd.DataFrame(json_data)
    df = df[df['zipCode'].isin(zipcodes)]
    estate_ids = df['estateId']

    return estate_ids

