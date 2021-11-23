import os, sys
from agent.boliga import (
    get_forsale_results,
    get_sold_results,
    get_estate_data
)
from agent.archive import (
    save_dict,
    read_ids_from_list_file,
    identify_ids_already_downloaded,
    identify_new_ids_to_download,
    load_dataframe_from_file,
    load_dataframe_from_dir
)
from agent.transform import (
    join_forsale_and_estate_data,
    join_sold_and_estate_data
)


def download_and_save_list_data(zipcode, forsale_path, sold_path):
    forsale_data = get_forsale_results(zipcode)
    save_dict(forsale_data, forsale_path)
    sold_data = get_sold_results(zipcode)
    save_dict(sold_data, sold_path)


def identify_new_estate_data(folder_root, forsale_path, sold_path):
    archive_ids = identify_ids_already_downloaded(folder_root)
    forsale_ids = read_ids_from_list_file(forsale_path)
    sold_ids = read_ids_from_list_file(sold_path)
    list_ids = forsale_ids.union(sold_ids)
    ids_to_download = identify_new_ids_to_download(list_ids, archive_ids)
    return ids_to_download


def download_new_estate_data(folder_root, ids_to_download):
    if len(ids_to_download) > 0:
        print(f'downloading estate data for {len(ids_to_download)} new items')
        new_data_list = [[eid, get_estate_data(eid)] for eid in ids_to_download]
        for li in new_data_list:
            save_path = f'{folder_root}/{li[0]}.gz'
            save_dict(li[1], save_path)


if __name__ == '__main__':

    zipcodes_to_process = [int(x) for x in sys.argv[1:] if x.isnumeric()]

    for zipcode in zipcodes_to_process:
        print(f'processing zipcode: {zipcode}')

        estate_path = f'./archive/{zipcode}/estate'
        forsale_path = f'./archive/{zipcode}/forsale.gz'
        sold_path = f'./archive/{zipcode}/sold.gz'

        #download_and_save_list_data(zipcode, forsale_path, sold_path)
        #ids = identify_new_estate_data(folder_root, forsale_path, sold_path)
        #download_new_estate_data(estate_path, ids)

        print(f'zipcode {zipcode} is now up to date!')

        df_forsale = load_dataframe_from_file(forsale_path)
        df_sold = load_dataframe_from_file(sold_path)
        df_estate = load_dataframe_from_dir(estate_path)

        df = join_forsale_and_estate_data(df_forsale, df_estate)
        df = join_sold_and_estate_data(df_sold, df_estate)
        print(df)
        break
