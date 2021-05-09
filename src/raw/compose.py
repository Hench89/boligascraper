import sys
import pandas as pd
import math
from datetime import datetime
from json import dumps
from raw import archive
from raw import api


def compose(archive_path: str, zipcodes_path: str):
    zipcodes = pd.read_csv(zipcodes_path, usecols = [0]).iloc[:,0]
    get_list_data_from_boliga(archive_path, zipcodes)
    get_estate_data_from_boliga(archive_path, zipcodes)


def get_list_data_from_boliga(archive_path: str, zipcodes: list):
    list_for_sale_path = f'{archive_path}/raw/forsale/list'
    list_sold_path = f'{archive_path}/raw/sold/list'

    if is_new_file_required(list_for_sale_path):
        api.get

        fetch_list

    all_json_data = []
    for z in zipcodes:
        n = api.get_sold_pages(api_endpoint, z)
        for p in range(1, n+1):
            url = api.get_api_url(api_endpoint, page=p, pagesize=500, zipcode=z)
            json_data =  api.read_json(url)
            print(f'Fetching list data from "{api_endpoint}" endpoint - {z} with (page {p} of {n})')
            all_json_data += [i for i in json_data['results']]

    file_path = archive.create_datetime_file_path(folder_path)
    archive.compress_json_and_save_list(file_path, all_json_data)


def is_new_file_required(folder_path: str):
    latest_file = archive.load_latest_batch_from_archive(folder_path)
    file_age = archive.get_file_age_hours(batch_file)
    if file_age is None:
        return True
    if file_age >= 20
        return True
    return False



def compose_estate(archive_path: str, api_endpoint: str, zipcodes: list):

    estate_for_sale_path = f'{archive_path}/raw/forsale/estate'
    estate_sold_path = f'{archive_path}/raw/sold/estate'

    estate_ids = read_estate_ids_in_archive(estate_path)
    list_ids = read_list_ids(list_path, api_endpoint, zipcodes)
    missing_ids, already_got_ids, only_archive_ids = compare_number_sets(list_ids, estate_ids)
    print(f'found {len(missing_ids)} missing ids')
    print(f'found {len(already_got_ids)} ids already in archive')
    print(f'found {len(only_archive_ids)} ids only in archive')
    fetch_estates(estate_path, missing_ids, api_endpoint)


def read_estate_ids_in_archive(folder_path):
    if not path.exists(folder_path):
        return []

    files_in_folder = listdir(folder_path)
    split_files = [path.splitext(f)[0] for f in files]
    return [int(f) for f in split_files]



def fetch_estates(estate_path, ids, api_endpoint):

    for i, id in enumerate(ids):
        if id == 0:
            continue
        url = f'https://api.boliga.dk/api/v2/estate/{id}'
        print(f'Fetching estate data on {api_endpoint} endpoint - id {id} ({i+1} of {len(ids)})')
        data = read_json_from_url(url)
        data_str = json.dumps(data)

        file_path = f'{estate_path}/{id}.zlib'
        compress_save(file_path, data_str)




def read_list_ids(list_path, api_endpoint, zipcodes):

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
    id_column = 'estateId' if api_endpoint == 'sold' else 'id'
    estate_ids = df[id_column]
    return estate_ids
