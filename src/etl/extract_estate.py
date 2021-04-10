import json
from utils import compress_save, decompresse_load, compare_number_sets, read_json_from_url
from os import listdir, path
import pandas as pd

def run(archive_path, zipcodes = []):

    # check inputs
    if len(zipcodes)==0:
        return print('.. zipcodes not configured correctly!')

    # fetch all estate ids
    subarchive_sold = archive_path + '/raw/sold'
    sold_estate_ids = read_estate_ids(subarchive_sold, zipcodes)

    # fetch archive ids
    subarchive_estate = archive_path + '/raw/estate'
    archive_ids = read_archive_ids(subarchive_estate)

    # determine what is missing
    missing, already_got, only_archive = compare_number_sets(sold_estate_ids, archive_ids)
    print(f'found {len(missing)} missing ids')
    print(f'found {len(already_got)} ids already in archive')
    print(f'found {len(only_archive)} ids only in archive')
    
    fetch_estates(subarchive_estate, missing)


def fetch_estates(archive_path, ids):

    def get_estate_url(estate_id):
        return f'https://api.boliga.dk/api/v2/estate/{estate_id}'

    for i, id in enumerate(ids):
        if id == 0:
            continue
        url = get_estate_url(id)
        print(f'Processing id {id} ({i+1} of {len(ids)})')
        estate_data = read_json_from_url(url)
        estate_json = json.dumps(estate_data)

        file_path = f'{archive_path}/{id}.zlib'
        compress_save(file_path, estate_json)


def read_archive_ids(archive_path):
    if not path.exists(archive_path):
        return []
    files = listdir(archive_path)
    split_files = [path.splitext(f)[0] for f in files]
    return [int(f) for f in split_files]


def read_estate_ids(archive_path, zipcodes):

    # get latest batch file
    files = listdir(archive_path)
    files.sort(reverse=True)
    latest_file = f'{archive_path}/{files[0]}'
    data = decompresse_load(latest_file)
    json_data = json.loads(data)
    
    # filtering
    df = pd.DataFrame(json_data)
    df = df[df['zipCode'].isin(zipcodes)]
    estate_ids = df['estateId']

    return estate_ids

