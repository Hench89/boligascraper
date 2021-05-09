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
    if is_new_file_required(list_for_sale_path):
        print('Getting new forsale list data!')
        data = api.get_list_data_from_zipcodes('forsale', zipcodes)
        archive.save_list_data(data, list_for_sale_path)

    list_sold_path = f'{archive_path}/raw/sold/list'
    if is_new_file_required(list_for_sale_path):
        print('Getting new sold list data!')
        api.get_list_data_from_zipcodes('sold', zipcodes)
        archive.save_list_data(data, list_sold_path)


def is_new_file_required(folder_path: str):
    latest_file = archive.load_latest_batch_from_archive(folder_path)
    if latest_file is None:
        return True
    file_age = archive.get_file_age_hours(latest_file)
    print(latest_file, file_age)
    if file_age is None:
        return True
    if file_age >= 20:
        return True
    return False


def get_estate_data_from_boliga(archive_path: str, zipcodes: list):

    list_for_sale_path = f'{archive_path}/raw/forsale/estate'
    list_ids = archive.read_ids_from_list_data(list_for_sale_path, zipcodes, 'id')

    estate_for_sale_path = f'{archive_path}/raw/forsale/estate'
    estate_ids = archive.read_estate_ids(estate_for_sale_path)

    list_for_sale_path = f'{archive_path}/raw/sold/estate'
    list_ids = archive.read_ids_from_list_data(list_for_sale_path, zipcodes, 'estateId')

    estate_for_sale_path = f'{archive_path}/raw/sold/estate'
    estate_ids = archive.read_estate_ids(estate_for_sale_path)



    estate_ids = read_estate_ids_in_archive(estate_path)
    list_ids = read_list_ids(list_path, api_endpoint, zipcodes)

    missing_ids, already_got_ids, only_archive_ids = compare_number_sets(list_ids, estate_ids)

    def compare_number_sets(list_a, list_b):

        if list_a is None or list_b is None:
            return list_a or [], list_b or []

        # cast as sets
        seta = set(list_a)
        setb = set(list_b)

        # find differences
        a_set_only = seta.difference(setb)
        set_intersection = setb.intersection(seta)
        b_set_only = setb.difference(seta)

        return list(a_set_only), list(set_intersection), list(b_set_only)



    print(f'found {len(missing_ids)} missing ids')
    print(f'found {len(already_got_ids)} ids already in archive')
    print(f'found {len(only_archive_ids)} ids only in archive')
    fetch_estates(estate_path, missing_ids, api_endpoint)



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

