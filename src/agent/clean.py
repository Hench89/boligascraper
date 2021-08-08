import pandas as pd
from agent.boliga import BoligaEstate
from archive import Archive


def clean_forsale_list():
    archive = Archive()
    df = archive.read_forsale_list()
    df = df.rename(columns={'id' : 'estateId'})
    column_dict = get_column_dict(df.columns)
    df = df[column_dict.keys()]
    df = df.rename(columns=column_dict)
    df['rooms'] = df['rooms'].astype(int)
    df.to_csv(archive.clean_forsale_list, index=False)
    print('cleaned forsale list data!')


def clean_sold_list():
    archive = Archive()
    df = archive.read_sold_list()
    df = df.rename(columns={'price' : 'sold_price'})
    column_dict = get_column_dict(df.columns)
    df = df[column_dict.keys()]
    df = df.rename(columns=column_dict)
    df['sqm_price'] = round(df['sqm_price']).astype(int)
    df['rooms'] = df['rooms'].astype(int)
    df.to_csv(archive.clean_sold_list, index=False)
    print('cleaned sold list data!')


def clean_forsale_estate():
    archive = Archive()
    df = archive.read_all_forsale_estate()
    df = df.drop('estateId', axis=1)
    df = df.rename(columns={'id' : 'estateId'})
    column_dict = get_column_dict(df.columns)
    df = df[column_dict.keys()]
    df = df.rename(columns=column_dict)
    df['rooms'] = df['rooms'].astype(int)
    df.to_csv(archive.clean_forsale_estate, index=False)
    print('cleaned forsale estate data!')


def clean_sold_estate():
    archive = Archive()
    df = archive.read_all_sold_estate()
    df = df.drop('estateId', axis=1)
    df = df.rename(columns={'id' : 'estateId'})
    column_dict = get_column_dict(df.columns)
    df = df[column_dict.keys()]
    df = df.rename(columns=column_dict)
    df['rooms'] = df['rooms'].astype(int)
    df.to_csv(archive.clean_sold_estate, index=False)
    print('cleaned sold estate data!')


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


def merge_forsale_data():
    archive = Archive()
    boliga_estate = BoligaEstate()
    df_list, df_estate = archive.read_clean_forsale_data()
    df_details = df_estate[['estate_id', 'estate_url', 'clean_street']]
    df_type = boliga_estate.get_property_master_data()
    df = df_list.copy()
    df = pd.merge(df, df_type, how='left', on='property_type')
    df = pd.merge(df, df_details, how='left', on='estate_id')
    df.to_csv(archive.clean_forsale_baseline, index=False)
    print('merged forsale data!')


def merge_sold_data():
    archive = Archive()
    df_list, df_estate = archive.read_clean_sold_data()
    list_cols = [
        'estate_id',
        'address',
        'sold_price',
        'sold_date',
        'sale_type',
        'property_type',
        'sqm_price',
        'rooms',
        'living_area',
        'lat',
        'lon'
    ]
    estate_cols = [
        'estate_id',
        'city',
        'zip_code',
        'lat',
        'lon',
        'build_year',
        'living_area',
        'lot_area',
        'bsmnt_area',
        'rooms',
        'floor',
        'energy_class',
        'net',
        'exp',
        'created_date',
        'sqm_price',
        'price_change',
        'list_price',
        'days_for_sale'
    ]
    df_list, df_estate = df_list[list_cols], df_estate[estate_cols]
    df = pd.merge(df_list, df_estate, how='left', on='estate_id')

    boliga_estate = BoligaEstate()
    df_type = boliga_estate.get_property_master_data()
    df = pd.merge(df, df_type, how='left', on='property_type')

    def coalesce(df, col):
        df[col] = df[f'{col}_x'].combine_first(df[f'{col}_y'])
        df = df.drop(columns=[f'{col}_x', f'{col}_y'])
        return df

    df = coalesce(df, 'sqm_price')
    df = coalesce(df, 'rooms')
    df = coalesce(df, 'living_area')
    df = coalesce(df, 'lat')
    df = coalesce(df, 'lon')

    df['price_diff'] = df['list_price'] - df['sold_price']

    df.to_csv(archive.clean_sold_baseline, index=False)
    print('merged sold data!')



if __name__ == "__main__":
    clean_forsale_list()
    clean_forsale_estate()
    clean_sold_list()
    clean_sold_estate()
    merge_forsale_data()
    merge_sold_data()
