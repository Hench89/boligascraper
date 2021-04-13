from .utils import load_json_folder, load_json_file, get_latest_file
from os import path, makedirs
import pandas as pd


def compose(root_path):

    print(f'===== CLEANING =====')

    # prepare clean folder
    clean_path = f'{root_path}/clean'
    if not path.exists(clean_path):
        makedirs(clean_path)

    # clean sold list
    raw_list_sold_path = f'{root_path}/raw/sold/list'
    latest_file_path = get_latest_file(raw_list_sold_path)
    clean_sold_list(latest_file_path, clean_path)

    # clean sold estates
    raw_estate_sold_path = f'{root_path}/raw/sold/estate'
    clean_sold_estate(raw_estate_sold_path, clean_path)

    # clean for sale list
    raw_list_for_sale_path = f'{root_path}/raw/forsale/list'
    latest_file_path = get_latest_file(raw_list_for_sale_path)
    clean_for_sale_list(latest_file_path, clean_path)

    # clean for sale estates
    raw_estate_for_sale_path = f'{root_path}/raw/sold/estate'
    clean_for_sale_estate(raw_estate_for_sale_path, clean_path)


def clean_sold_list(input_file_path, output_folder_path):

    # load file to dataframe
    list_dict = load_json_file(input_file_path)
    df = pd.DataFrame(list_dict)

    # initial renaming
    df = df.rename(columns={'price' : 'sold_price'})
    column_dict = get_column_dict(df.columns)
    df = df[column_dict.keys()]
    df = df.rename(columns=column_dict)

    # type casting
    df['sqm_price'] = round(df['sqm_price']).astype(int)
    df['rooms'] = df['rooms'].astype(int)

    # save file
    output_file_path = f'{output_folder_path}/clean_sold_list.json'
    df.to_json(output_file_path, orient='table')
    print(f'Saved {output_file_path}!')


def clean_sold_estate(input_folder_path, output_folder_path):

    # load folder to dataframe
    list_dict = load_json_folder(input_folder_path)
    df = pd.DataFrame(list_dict)

    # renaming
    df = df.drop('estateId', axis=1)
    df = df.rename(columns={'id' : 'estateId'})
    column_dict = get_column_dict(df.columns)
    df = df[column_dict.keys()]
    df = df.rename(columns=column_dict)

    # type casting
    df['rooms'] = df['rooms'].astype(int)

    # save file
    output_file_path = f'{output_folder_path}/clean_sold_estate.json'
    df.to_json(output_file_path, orient='table')
    print(f'Saved {output_file_path}!')


def clean_for_sale_list(input_file_path, output_folder_path):

    # load file to dataframe
    list_dict = load_json_file(input_file_path)
    df = pd.DataFrame(list_dict)

    # renaming
    df = df.rename(columns={'id' : 'estateId'})
    column_dict = get_column_dict(df.columns)
    df = df[column_dict.keys()]
    df = df.rename(columns=column_dict)

    # type casting
    df['rooms'] = df['rooms'].astype(int)

    # save file
    output_file_path = f'{output_folder_path}/clean_for_sale_list.json'
    df.to_json(output_file_path, orient='table')
    print(f'Saved {output_file_path}!')


def clean_for_sale_estate(input_folder_path, output_folder_path):

    # load folder to dataframe
    list_dict = load_json_folder(input_folder_path)
    df = pd.DataFrame(list_dict)

    # renaming
    column_dict = get_column_dict(df.columns)
    df = df[column_dict.keys()]
    df = df.rename(columns=column_dict)

    # type casting
    df['rooms'] = df['rooms'].astype(int)

    # save file
    output_file_path = f'{output_folder_path}/clean_for_sale_estate.json'
    df.to_json(output_file_path, orient='table')
    print(f'Saved {output_file_path}!')


def get_column_dict(dataset_keys):
    full_dict = {
        'estateId' : 'estate_id',
        'registeredArea' : 'area_id',
        'area' : 'area_category_id',
        'soldDate' : 'sold_date',
        'sold_price' : 'sold_price',
        'daysForSale' : 'days_for_sale',
        'estateUrl' : 'estate_url',
        'address' : 'address',
        'cleanStreet' : 'clean_street',
        'street' : 'street',
        'saleType' : 'sale_type',
        'latitude' : 'lat',
        'longitude' : 'lon',
        'propertyType' : 'property_type',
        'change' : 'price_change',
        'priceChangePercentTotal' : 'price_change',
        'energyClass' : 'energy_class',
        'price' : 'list_price',
        'rooms' : 'rooms',
        'size' : 'living_area',
        'lotSize' : 'lot_area',
        'floor' : 'floor',
        'buildYear' : 'build_year',
        'city' : 'city',
        'municipality' : 'municipality_code',
        'municipalityCode' : 'municipality_code',
        'zipCode' : 'zip_code',
        'squaremeterPrice' : 'sqm_price',
        'sqmPrice' : 'sqm_price',
        'createdDate' : 'created_date',
        'net' : 'net',
        'exp' : 'exp',
        'basementSize' : 'bsmnt_area'
    }
    filter_keys = [k for k in dataset_keys if k in full_dict.keys()]
    return {key: full_dict[key] for key in filter_keys}
