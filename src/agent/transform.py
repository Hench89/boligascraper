import pandas as pd
import numpy as np
import datetime
from agent import utils


def add_missing_cols_to_dataframe(df_source: pd.DataFrame, df_to_join: pd.DataFrame, key: str):
    cols_to_add = set(df_to_join.columns).difference(set(df_source.columns))
    cols_to_add_with_key = list(cols_to_add) + [key]
    df_to_join = df_to_join[cols_to_add_with_key]
    df = pd.merge(df_source, df_to_join, how='left', on=key)
    return df


def run_cleaning_steps(df: pd.DataFrame):
    df = filter_and_rename_boliga_columns(df)
    df = convert_selected_columns_to_int64(df)
    df = trim_non_alphabetical_values(df)
    df = add_urls(df)
    return df


def filter_and_rename_boliga_columns(df: pd.DataFrame):

    if 'estateId' in df.columns and 'id' in df.columns:
        df.drop('estateId', axis=1, inplace=True)  # for estate data id col is always 0

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
        'basementSize': 'basement_size',
        'soldDate' : 'sold_date',
        'saleType' : 'sale_type',
        'change' : 'price_change'
    }
    filter_cols = set(rename_dict.keys()).intersection(set(df.columns))
    df = df[filter_cols]
    df = df.rename(columns=rename_dict)
    return df


def convert_selected_columns_to_int64(df: pd.DataFrame):
    cols = [
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
    relevant_cols = set(cols).intersection(set(df.columns))
    for c in relevant_cols:
        df[c] = utils.convert_str_series_to_int64(df[c])
    return df


def trim_non_alphabetical_values(df: pd.DataFrame):
    cols = ['energy_class']
    relevant_cols = set(cols).intersection(set(df.columns))
    for c in relevant_cols:
        df[c] = utils.make_str_series_alphabetical(df[c])
    return df


def add_urls(df: pd.DataFrame):
    df['maps_url'] = df.apply(lambda x: f'https://www.google.com/maps?q={x.latitude},{x.longitude}', axis=1)
    df['boliga_url'] = df.apply(lambda x: f'https://www.boliga.dk/bolig/{x.estate_id}', axis=1)
    return df


def add_days_ago(df, from_col, column_name):
    now_days = pd.to_datetime(datetime.datetime.now())
    created_days = pd.to_datetime(df[from_col], format='%Y-%m-%dT%H:%M:%S.%fZ')
    time_delta = now_days - created_days
    time_delta_as_days = round(time_delta / np.timedelta64(1, "D"))
    df[column_name] = time_delta_as_days.astype(int)
    return df