import pandas as pd
from .utils import convert_str_to_int, remove_numbers_and_special


def join_forsale_and_estate_data(df_list: pd.DataFrame, df_estate: pd.DataFrame) -> pd.DataFrame:
    estate_cols = ['estate_id', 'estate_url', 'clean_street_name']
    df_estate = df_estate[estate_cols]
    df = df_list.copy()
    df = pd.merge(df, df_estate, how='left', on='estate_id')
    return df


def join_sold_and_estate_data(df_list: pd.DataFrame, df_estate: pd.DataFrame) -> pd.DataFrame:
    estate_cols = [
        'estate_id',
        'clean_street_name',
        'exp',
        'floor',
        'energy_class',
        'created_date',
        'basement_size',
        'is_active',
        'estate_url',
        'net',
        'sqm_price',
        'lot_size',
        'street_name',
        'price_change_pct_total'
    ]
    df_estate = df_estate[estate_cols]
    df = df_list.copy()
    df = pd.merge(df, df_estate, how='left', on='estate_id')
    return df


def add_missing_cols_to_dataframe(df_source: pd.DataFrame, df_to_join: pd.DataFrame, key: str):
    cols_to_add = set(df_to_join.columns).difference(set(df_source.columns))
    cols_to_add_with_key = list(cols_to_add) + [key]
    df_to_join = df_to_join[cols_to_add_with_key]
    df = pd.merge(df_source, df_to_join, how='left', on=key)
    return df


def filter_and_rename_boliga_columns(df: pd.DataFrame):

    if 'estateId' in df.columns and 'id' in df.columns:
        df.drop('estateId', axis=1, inplace=True)  # estate data id col which is always 0

    rename_dict = {
        'estateUrl': 'estate_url',
        'cleanStreet': 'clean_street_name',
        'id': 'estate_id',
        'estateId': 'estate_id',
        'latitude': 'latitude',
        'longitude': 'longitude',
        'propertyType': 'property_type',
        'priceChangePercentTotal': 'price_change_pct_total',
        'energyClass': 'energy_class',
        'price': 'price',
        'rooms': 'rooms',
        'size': 'living_area_size',
        'lotSize': 'lot_size',
        'floor': 'floor',
        'buildYear': 'construction_year',
        'city': 'city',
        'isActive': 'is_active',
        'zipCode': 'zipcode',
        'street': 'street_name',
        'squaremeterPrice': 'sqm_price',
        'createdDate': 'created_date',
        'net': 'net',
        'exp': 'exp',
        'basementSize': 'basement_size'
    }
    filter_cols = set(rename_dict.keys()).intersection(set(df.columns))
    df = df[filter_cols]
    df = df.rename(columns=rename_dict)
    return df


def convert_types_in_estate_data(df: pd.DataFrame):
    int_cols = [
        'estate_id',
        'price',
        'rooms',
        'living_area_size',
        'lot_size',
        'floor',
        'zipcode',
        'net',
        'exp',
        'construction_year',
        'basement_size',
        'sqm_price'
    ]
    alphabet_cols = ['energy_class']
    relevant_int_cols = set(int_cols).intersection(set(df.columns))
    relevant_alphabet_cols = set(alphabet_cols).intersection(set(df.columns))

    for c in relevant_int_cols:
        df[c] = df.apply(lambda x: convert_str_to_int(x[c]), axis=1)
    for c in relevant_alphabet_cols:
        df[c] = df.apply(lambda x: remove_numbers_and_special(x[c]), axis=1)


    return df
