import os, sys, csv
from agent import boliga, archive, transform, utils


def get_paths(zipcode):
    return {
        'forsale_path': f'./archive/{zipcode}/forsale_raw.gz',
        'sold_path': f'./archive/{zipcode}/sold_raw.gz',
        'estate_dir': f'./archive/{zipcode}/estate_raw',
        'forsale_parquet': f'./archive/{zipcode}/clean/forsale.parquet',
        'forsale_csv': f'./archive/{zipcode}/clean/forsale.csv',
        'sold_parquet': f'./archive/{zipcode}/clean/sold.parquet',
        'sold_csv': f'./archive/{zipcode}/clean/sold.csv'
    }


def download_and_save_list_data(zipcode, forsale_path, sold_path):
    paths = [forsale_path, sold_path]
    apis = ['forsale', 'sold']
    for path, api in zip(paths, apis):
        data = boliga.get_list_results(zipcode, api)
        archive.save_dict(data, path)


def identify_estate_data_to_download(forsale_path, sold_path, estate_dir):
    estate_ids = archive.identify_estate_ids_already_downloaded(estate_dir)
    forsale_ids = archive.read_ids_from_list_file(forsale_path, 'forsale')
    sold_ids = archive.read_ids_from_list_file(sold_path, 'sold')
    all_list_ids = forsale_ids.union(sold_ids)
    ids_to_download = archive.identify_new_ids_to_download(all_list_ids, estate_ids)
    return ids_to_download


def download_new_estate_data(ids_to_download, estate_dir):
    if len(ids_to_download) > 0:
        print(f'downloading estate data for {len(ids_to_download)} new items')
        for idx, estate_id in enumerate(ids_to_download):
            idx_to_go = len(ids_to_download) - idx
            if (idx_to_go % 100) == 0:
                print(f'{idx_to_go} more to go..')
            data = boliga.get_estate_data(estate_id)
            estate_path = f'{estate_dir}/{estate_id}.gz'
            archive.save_dict(data, estate_path)


def read_and_clean_data(forsale_path, sold_path, estate_dir):
    df_forsale = archive.load_dataframe_from_file(forsale_path)
    df_forsale = transform.run_cleaning_steps(df_forsale)
    df_sold = archive.load_dataframe_from_file(sold_path)
    df_sold = transform.run_cleaning_steps(df_sold)
    df_estate = archive.load_dataframe_from_dir(estate_dir)
    df_estate = transform.run_cleaning_steps(df_estate)
    return df_forsale, df_sold, df_estate


def merge_data_and_save_to_file(df1, df2, parquet_path, csv_path):
    df = transform.add_missing_cols_to_dataframe(df1, df2, 'estate_id')
    for p in [parquet_path, csv_path]:
        utils.create_dirs_for_file(p)
    df.to_parquet(parquet_path)
    df.to_csv(csv_path, encoding='utf-8-sig', quoting=csv.QUOTE_NONNUMERIC )


def download_new_data(zipcode):
    paths = get_paths(zipcode)
    path01 = paths['forsale_path']
    path02 = paths['sold_path']
    path03 = paths['estate_dir']
    download_and_save_list_data(zipcode, path01, path02)
    ids = identify_estate_data_to_download(path01, path02, path03)
    download_new_estate_data(ids, path03)


def clean_data(zipcode):
    paths = get_paths(zipcode)
    path01 = paths['forsale_path']
    path02 = paths['sold_path']
    path03 = paths['estate_dir']
    path04 = paths['forsale_parquet']
    path05 = paths['forsale_csv']
    path06 = paths['sold_parquet']
    path07 = paths['sold_csv']
    df_forsale, df_sold, df_estate = read_and_clean_data(path01, path02, path03)
    merge_data_and_save_to_file(df_forsale, df_estate, path04, path05)
    merge_data_and_save_to_file(df_sold, df_estate, path06, path07)


if __name__ == '__main__':
    zipcodes_to_process = [int(x) for x in sys.argv[1:] if x.isnumeric()]
    for zipcode in zipcodes_to_process:
        print(f'processing zipcode: {zipcode}')
        download_new_data(zipcode)
        clean_data(zipcode)
