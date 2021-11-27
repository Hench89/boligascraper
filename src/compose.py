import os, sys, csv
from agent import boliga, archive, transform, utils


def download_and_save_list_data(zipcode, forsale_path, sold_path):
    forsale_data = boliga.get_forsale_results(zipcode)
    archive.save_dict(forsale_data, forsale_path)
    sold_data = boliga.get_sold_results(zipcode)
    archive.save_dict(sold_data, sold_path)


def download_new_estate_data(folder_root, forsale_path, sold_path):
    archive_ids = archive.identify_ids_already_downloaded(folder_root)
    forsale_ids = archive.read_ids_from_list_file(forsale_path, 'id')
    sold_ids = archive.read_ids_from_list_file(sold_path, 'estateId')
    list_ids = forsale_ids.union(sold_ids)
    ids_to_download = archive.identify_new_ids_to_download(list_ids, archive_ids)
    if len(ids_to_download) > 0:
        print(f'downloading estate data for {len(ids_to_download)} new items')
        for idx, i in enumerate(ids_to_download):
            idx_to_go = len(ids_to_download) - idx
            if (idx_to_go % 100) == 0:
                print(f'{idx_to_go} more to go..')
            data = boliga.get_estate_data(i)
            save_path = f'{folder_root}/{i}.gz'
            archive.save_dict(data, save_path)


def read_and_clean_data(forsale_path, sold_path, estate_path):
    df_forsale = archive.load_dataframe_from_file(forsale_path)
    df_forsale = transform.run_cleaning_steps(df_forsale)
    df_sold = archive.load_dataframe_from_file(sold_path)
    df_sold = transform.run_cleaning_steps(df_sold)
    df_estate = archive.load_dataframe_from_dir(estate_path)
    df_estate = transform.run_cleaning_steps(df_estate)
    return df_forsale, df_sold, df_estate


def merge_data_and_save_to_file(df1, df2, parquet_path, csv_path):
    df = transform.add_missing_cols_to_dataframe(df1, df2, 'estate_id')
    for p in [parquet_path, csv_path]:
        utils.create_dirs_for_file(p)
    df.to_parquet(parquet_path)
    df.to_csv(csv_path, encoding='utf-8-sig', quoting=csv.QUOTE_NONNUMERIC )


if __name__ == '__main__':
    zipcodes_to_process = [int(x) for x in sys.argv[1:] if x.isnumeric()]

    for zipcode in zipcodes_to_process:
        print(f'processing zipcode: {zipcode}')

        path01 = f'./archive/{zipcode}/forsale_raw.gz'
        path02 = f'./archive/{zipcode}/sold_raw.gz'
        path03 = f'./archive/{zipcode}/estate_raw'
        path04 = f'./archive/{zipcode}/clean/forsale.parquet'
        path05 = f'./archive/{zipcode}/clean/forsale.csv'
        path06 = f'./archive/{zipcode}/clean/sold.parquet'
        path07 = f'./archive/{zipcode}/clean/sold.csv'

        download_and_save_list_data(zipcode, path01, path02)
        download_new_estate_data(path03, path01, path02)
        df_forsale, df_sold, df_estate = read_and_clean_data(path01, path02, path03)
        merge_data_and_save_to_file(df_forsale, df_estate, path04, path05)
        merge_data_and_save_to_file(df_sold, df_estate, path06, path07)
