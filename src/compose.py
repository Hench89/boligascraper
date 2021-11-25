import os, sys
from agent import boliga, archive, transform


def download_and_save_list_data(zipcode, forsale_path, sold_path):
    forsale_data = boliga.get_forsale_results(zipcode)
    archive.save_dict(forsale_data, forsale_path)
    sold_data = boliga.get_sold_results(zipcode)
    archive.save_dict(sold_data, sold_path)


def identify_new_estate_data(folder_root, forsale_path, sold_path):
    archive_ids = archive.identify_ids_already_downloaded(folder_root)
    forsale_ids = archive.read_ids_from_list_file(forsale_path, 'id')
    sold_ids = archive.read_ids_from_list_file(sold_path, 'estateId')
    list_ids = forsale_ids.union(sold_ids)
    ids_to_download = archive.identify_new_ids_to_download(list_ids, archive_ids)
    return ids_to_download


def download_new_estate_data(folder_root, ids_to_download):
    if len(ids_to_download) > 0:
        print(f'downloading estate data for {len(ids_to_download)} new items')
        for i in ids_to_download:
            data = boliga.get_estate_data(i)
            save_path = f'{folder_root}/{i}.gz'
            archive.save_dict(data, save_path)


def load_and_make_data_clean(path, load_dir=False):
    if load_dir:
        df = archive.load_dataframe_from_dir(path)
    else:
        df = archive.load_dataframe_from_file(path)
    df = transform.filter_and_rename_boliga_columns(df)
    df = transform.convert_types_in_estate_data(df)
    return df

def transform_and_save_data(df1, df2, key, save_path):
    df = transform.add_missing_cols_to_dataframe(df1, df2, key)
    df.to_csv(save_path, encoding='utf-8-sig')


def read_and_clean_data(forsale_path, sold_path, estate_path, forsale_clean_path, sold_clean_path):
    df_forsale = load_and_make_data_clean(forsale_path)
    df_sold = load_and_make_data_clean(sold_path)
    df_estate = load_and_make_data_clean(estate_path, load_dir=True)
    transform_and_save_data(df_forsale, df_estate, 'estate_id', forsale_clean_path)
    transform_and_save_data(df_sold, df_estate, 'estate_id', sold_clean_path)


if __name__ == '__main__':
    zipcodes_to_process = [int(x) for x in sys.argv[1:] if x.isnumeric()]

    for zipcode in zipcodes_to_process:
        print(f'processing zipcode: {zipcode}')

        estate_path = f'./archive/{zipcode}/estate'
        forsale_path = f'./archive/{zipcode}/forsale.gz'
        sold_path = f'./archive/{zipcode}/sold.gz'
        forsale_clean_path = f'./archive/{zipcode}/forsale.csv'
        sold_clean_path = f'./archive/{zipcode}/sold.csv'

        download_and_save_list_data(zipcode, forsale_path, sold_path)
        ids = identify_new_estate_data(estate_path, forsale_path, sold_path)
        download_new_estate_data(estate_path, ids)
        read_and_clean_data(forsale_path, sold_path, estate_path, forsale_clean_path, sold_clean_path)
