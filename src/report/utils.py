import pandas as pd
import numpy as np
import datetime


def fix_pricing(price):
    if pd.isna(price):
        return '-'
    price = int(price)
    price = '{:,}'.format(price)
    price = price.replace(',', '.')
    return str(price)


def add_days_ago(df, from_col, column_name):
    now_days = pd.to_datetime(datetime.datetime.now())
    created_days = pd.to_datetime(df[from_col], format='%Y-%m-%dT%H:%M:%S.%fZ')
    time_delta = now_days - created_days
    time_delta_as_days = round(time_delta / np.timedelta64(1, "D"))
    df[column_name] = time_delta_as_days.astype(int)
    return df


def set_url(estate_id):
    if estate_id == 0:
        return '-'
    return f'https://www.boliga.dk/bolig/{estate_id}' if estate_id != 0 else ''


def get_property_types():
    data = [
        [1, 'Villa', 'V'],
        [2, 'Rækkehus', 'R'],
        [3, 'Ejerlejlighed', 'E'],
        [4, 'Fritidshus', 'F'],
        [5, 'Andelsbolig', 'A'],
        [6, 'Landejendom', 'L'],
        [7, 'Helårsgrund', 'G'],
        [8, 'Fritidsgrund', 'G'],
        [9, 'Villalejlighed', 'VI'],
        [10, 'Andet', 'A']
    ]
    cols = ['property_id', 'property_name', 'alias']
    return pd.DataFrame(data, columns = cols)
