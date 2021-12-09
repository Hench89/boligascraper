import os, sys, csv
from datetime import date
from agent import boliga, archive, transform, utils
import pandas as pd


def identify_estate_data_to_download(forsale_path, sold_path, estate_dir):
    estate_ids = archive.identify_estate_ids_already_downloaded(estate_dir)
    forsale_ids = archive.read_ids_from_list_file(forsale_path, 'forsale')
    sold_ids = archive.read_ids_from_list_file(sold_path, 'sold')
    all_list_ids = forsale_ids.union(sold_ids)
    ids_to_download = archive.identify_new_ids_to_download(all_list_ids, estate_ids)
    return ids_to_download


def read_and_clean_dataframe(path):
    if os.path.isdir(path):
        df = archive.load_dataframe_from_dir(path)
    else:
        df = archive.load_dataframe_from_file(path)
    df = transform.run_cleaning_steps(df)
    return df


def merge_data_and_save_to_file(df1, df2, dir_path, filename):
    parquet_path = f'{dir_path}/{filename}.parquet'
    csv_path = f'{dir_path}/{filename}.csv'
    utils.create_dirs_for_file(csv_path)
    df = transform.add_missing_cols_to_dataframe(df1, df2, 'estate_id')
    df.to_parquet(parquet_path)
    df.to_csv(csv_path, encoding='utf-8-sig', quoting=csv.QUOTE_NONNUMERIC )


def download_new_estate_data(zipcode, forsale_path, sold_path, estate_dir):
    ids = identify_estate_data_to_download(forsale_path, sold_path, estate_dir)
    if len(ids) > 0:
        print(f'downloading estate data for {len(ids)} new items')
        for idx, estate_id in enumerate(ids):
            idx_to_go = len(ids) - idx
            if (idx_to_go % 100) == 0:
                print(f'{idx_to_go} more to go..')
            data = boliga.get_estate_data(estate_id)
            data['fetched_date'] = str(date.today())
            estate_path = f'{path03}/{estate_id}.gz'
            archive.save_dict(data, estate_path)


def download_new_list_data(zipcode, forsale_path, sold_path):
    apis = ['forsale', 'sold']
    paths = [forsale_path, sold_path]
    for path, api in zip(paths, apis):
        data = boliga.get_list_results(zipcode, api)
        archive.save_dict(data, path)


def download_data(zipcode, forsale_path, sold_path, estate_dir):
    print(f'downloading data for zipcode {zipcode}')
    download_new_list_data(zipcode, forsale_path, sold_path)
    download_new_estate_data(zipcode, forsale_path, sold_path, estate_dir)


def read_dataframe_from_paths(paths):
    dfs = [read_and_clean_dataframe(p) for p in paths]
    df = pd.concat(dfs)
    return df


if __name__ == '__main__':

    zipcodes = [int(x) for x in sys.argv[1:] if x.isnumeric()]
    forsale_files = {z: f'./archive/{z}/forsale_raw.gz' for z in zipcodes}
    sold_files = {z: f'./archive/{z}/sold_raw.gz' for z in zipcodes}
    estate_dirs = {z: f'./archive/{z}/estate_raw' for z in zipcodes}

    for z in zipcodes:
        download_data(z, forsale_files[z], sold_files[z], estate_dirs[z])

    df_forsale = read_dataframe_from_paths(forsale_files.values())
    df_sold = read_dataframe_from_paths(sold_files.values())
    df_estate = read_dataframe_from_paths(estate_dirs.values())

    merge_data_and_save_to_file(df_forsale, df_estate, './archive', 'forsale')
    merge_data_and_save_to_file(df_sold, df_estate, './archive', 'sold')
