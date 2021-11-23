import pandas as pd


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

