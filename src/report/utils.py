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
