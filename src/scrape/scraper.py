'''Maintain local archive for boliga data.

Fetch all raw sold/for sale data from boliga within a set of zipcodes.
Remove entries that no longer exist.
'''

import sys
from datetime import date
from utils import io
import boliga_api
from schema import ListItem

def identify_missing_and_removed_ids(forsale_path, sold_path, estate_dir):
    estate_ids = io.identify_estate_ids_already_downloaded(estate_dir)
    forsale_ids = io.read_ids_from_list_file(forsale_path, 'forsale')
    sold_ids = io.read_ids_from_list_file(sold_path, 'sold')
    all_list_ids = forsale_ids.union(sold_ids)
    missing_ids = set(all_list_ids).difference(set(estate_ids))
    removed_ids = set(estate_ids).difference(set(all_list_ids))
    missing_ids.remove(0)  # id 0 for estates without proper data
    return missing_ids, removed_ids


def download_new_estate_data(ids, estate_dir):
    for idx, estate_id in enumerate(ids):
        idx_to_go = len(ids) - idx
        if (idx_to_go % 100) == 0:
            print(f'{idx_to_go} more to go..')
        data = boliga_api.get_estate_data(estate_id)
        data['fetched_date'] = str(date.today())
        estate_path = f'{estate_dir}/{estate_id}.gz'
        io.save_dict(data, estate_path)


def download_new_list_data(zipcode, api_name, path):

    results = boliga_api.get_list_results(zipcode, api_name)
    for raw_dict in results:
    
        filtered_dict = {k: raw_dict[k] for k in ListItem().raw_fields}
        filtered_dict['list_type'] = api_name

        print(filtered_dict)
        list_item = ListItem(**filtered_dict)
        print(list_item)
    
    io.save_dict(data, path)


def process_zipcode(zipcode, forsale_path, sold_path, estate_dir):

    print('.. downloading list data')
    download_new_list_data(zipcode, api_name='forsale', path=forsale_path)
    download_new_list_data(zipcode, api_name='sold', path=sold_path)
    missing_ids, removed_ids = identify_missing_and_removed_ids(forsale_path, sold_path, estate_dir)

    if len(missing_ids) > 0:
        print(f'.. downloading data for {len(missing_ids)} new estate(s)')
        download_new_estate_data(missing_ids, estate_dir)

    if len(removed_ids) > 0:
        print(f'.. deleting data for {len(removed_ids)} estate(s)')
        io.delete_files(estate_dir, removed_ids)



def main():

    zipcodes = [int(x) for x in sys.argv[1:] if x.isnumeric()]
    for zipcode in zipcodes:
        forsale_file = f'./archive/{zipcode}/forsale_raw.gz'
        sold_file = f'./archive/{zipcode}/sold_raw.gz'
        estate_dir = f'./archive/{zipcode}/estate_raw'
        
        print(f'processing zipcode {zipcode}')
        process_zipcode(zipcode, forsale_file, sold_file, estate_dir)


if __name__ == '__main__':
    main()
