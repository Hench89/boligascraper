import pandas as pd
from archive import RawArchive


def clean_forsale_list(df, output_file_path):
    df = df.rename(columns={'id' : 'estateId'})
    column_dict = get_column_dict(df.columns)
    df = df[column_dict.keys()]
    df = df.rename(columns=column_dict)
    df['rooms'] = df['rooms'].astype(int)
    df.to_csv(output_file_path, index=False)


def clean_sold_list(df, output_file_path):
    df = df.rename(columns={'price' : 'sold_price'})
    column_dict = get_column_dict(df.columns)
    df = df[column_dict.keys()]
    df = df.rename(columns=column_dict)
    df['sqm_price'] = round(df['sqm_price']).astype(int)
    df['rooms'] = df['rooms'].astype(int)
    df.to_csv(output_file_path, index=False)


def clean_forsale_estate(df, output_file_path):
    df = df.drop('estateId', axis=1)
    df = df.rename(columns={'id' : 'estateId'})
    column_dict = get_column_dict(df.columns)
    df = df[column_dict.keys()]
    df = df.rename(columns=column_dict)
    df['rooms'] = df['rooms'].astype(int)
    df.to_csv(output_file_path, index=False)


def clean_sold_estate(df, output_file_path):
    df = df.drop('estateId', axis=1)
    df = df.rename(columns={'id' : 'estateId'})
    column_dict = get_column_dict(df.columns)
    df = df[column_dict.keys()]
    df = df.rename(columns=column_dict)
    df['rooms'] = df['rooms'].astype(int)
    df.to_csv(output_file_path, index=False)


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
        'street' : 'address',
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
        'basementSize' : 'bsmnt_area',
        'isActive' : 'is_active'
    }
    filter_keys = [k for k in dataset_keys if k in full_dict.keys()]
    return {key: full_dict[key] for key in filter_keys}


if __name__ == "__main__":
    archive = RawArchive()

    df = archive.read_forsale_list()
    file_path = './archive/clean_forsale_list'
    clean_forsale_list(df, file_path)
    print(f'Saved {file_path}!')

    df = archive.read_all_forsale_estate()
    file_path = './archive/clean_forsale_estate'
    clean_forsale_estate(df, file_path)
    print(f'Saved {file_path}!')

    df = archive.read_sold_list()
    file_path = './archive/clean_sold_list'
    clean_sold_list(df, file_path)
    print(f'Saved {file_path}!')

    df = archive.read_all_sold_estate()
    file_path = './archive/clean_sold_estate'
    clean_sold_estate(df, file_path)
    print(f'Saved {file_path}!')