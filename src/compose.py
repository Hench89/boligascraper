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
    identify_new_ids_to_download
)


if __name__ == '__main__':

    zipcodes_to_process = [int(x) for x in sys.argv[1:] if x.isnumeric()]

    for zipcode in zipcodes_to_process:

        print(f'processing zipcode: {zipcode}')
        folder_root = f'./archive/{zipcode}'
        forsale_path = f'./archive/{zipcode}/forsale.gz'
        sold_path = f'./archive/{zipcode}/sold.gz'

        print('downloading new list data')
        forsale_data = get_forsale_results(zipcode)
        save_dict(forsale_data, forsale_path)
        sold_data = get_sold_results(zipcode)
        save_dict(sold_data, sold_path)

        archive_ids = identify_ids_already_downloaded(folder_root)
        forsale_ids = read_ids_from_list_file(forsale_path)
        sold_ids = read_ids_from_list_file(sold_path)
        list_ids = forsale_ids.union(sold_ids)
        ids_to_download = identify_new_ids_to_download(list_ids, archive_ids)

        if len(ids_to_download) > 0:
            print(f'downloading estate data for {len(ids_to_download)} new items')
            new_data_list = [[eid, get_estate_data(eid)] for eid in ids_to_download]
            for li in new_data_list:
                save_path = f'{folder_root}/{li[0]}.gz'
                save_dict(li[1], save_path)

        print(f'zipcode {zipcode} is up to date!')
