import sys
from datetime import date
from utils import io
import boliga_api
from schema import ListItem
from folder_archive import FolderArchive


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


def download_new_list_data(zipcode, api_name, list_path, folder_archive):
    print('.. downloading list data')
    results = boliga_api.get_list_results(zipcode, api_name)

    list_items = []
    for result_item in results:
        filtered_result = {k: result_item[k] for k in ListItem().input_fields}
        filtered_result['list_type'] = api_name
        list_items.append(ListItem(**filtered_result))

    folder_archive.save_list_result(list_items, list_path)


def process_zipcode(zipcode, forsale_path, sold_path, estate_dir):

    missing_ids, removed_ids = identify_missing_and_removed_ids(forsale_path, sold_path, estate_dir)

    if len(missing_ids) > 0:
        print(f'.. downloading data for {len(missing_ids)} new estate(s)')
        download_new_estate_data(missing_ids, estate_dir)

    if len(removed_ids) > 0:
        print(f'.. deleting data for {len(removed_ids)} estate(s)')
        io.delete_files(estate_dir, removed_ids)


def main():

    zipcodes = [int(x) for x in sys.argv[1:] if x.isnumeric()]
    folder_archive = FolderArchive()
    for zipcode in zipcodes:

        print(f'processing zipcode {zipcode}')
        endpoints = [
            ('forsale', f'./archive/{zipcode}/forsale_raw'),
            ('sold', f'./archive/{zipcode}/sold_raw')
        ]
        for endpoint_name, file_path in endpoints:
            download_new_list_data(zipcode, endpoint_name, file_path, folder_archive)


if __name__ == '__main__':
    main()
