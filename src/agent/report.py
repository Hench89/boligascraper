import pandas as pd
import numpy as np
import datetime
from archive import Archive
from email_util import get_html_df, send_email


def prepare_forsale():
    archive = Archive()
    df = archive.read_forsale_baseline()

    df = df[df['alias'].isin(['V','R'])]
    df = add_days_ago(df, 'created_date', 'days')
    df = df[df['days'] < 30]

    df['maps_url'] = df.apply(lambda x: f'https://www.google.com/maps?q={x.lat},{x.lon}', axis=1)
    df['boliga_url'] = df.apply(lambda x: f'https://www.boliga.dk/bolig/{x.estate_id}', axis=1)
    df['city'] = df.apply(lambda x: 'Lyngby' if x.city == 'Kongens Lyngby' else x.city, axis=1)
    df['list_price'] = df.apply(lambda x: fix_pricing(x.list_price), axis=1)
    df['sqm_price'] = df.apply(lambda x: fix_pricing(x.sqm_price), axis=1)

    cols = [
        'city',
        'address',
        'alias',
        'rooms',
        'living_area',
        'lot_area',
        'energy_class',
        'build_year',
        'list_price',
        'sqm_price',
        'boliga_url',
        'estate_url',
        'maps_url',
        'days'
    ]
    df = df[cols]
    df = df.sort_values(by=['city', 'days']).reset_index(drop=True)

    return df


def prepare_sold():
    archive = Archive()
    df = archive.read_sold_baseline()

    df = df[df['alias'].isin(['V','R'])]
    df = df[df['sale_type'] == 'Alm. Salg']

    df = add_days_ago(df, 'sold_date', 'days')
    df['boliga_url'] = df.apply(lambda x: add_boliga_url(x.estate_id), axis=1)
    df['maps_url'] = df.apply(lambda x: f'https://www.google.com/maps?q={x.lat},{x.lon}', axis=1)
    df['price_diff'] = df.apply(lambda x: fix_pricing(x.price_diff), axis=1)
    df['list_price'] = df.apply(lambda x: fix_pricing(x.list_price), axis=1)
    df['sold_price'] = df.apply(lambda x: fix_pricing(x.sold_price), axis=1)
    df['sqm_price'] = df.apply(lambda x: fix_pricing(x.sqm_price), axis=1)

    cols = [
        'city',
        'address',
        'alias',
        'rooms',
        'living_area',
        'energy_class',
        'build_year',
        'list_price',
        'sold_price',
        'sqm_price',
        'price_diff',
        'boliga_url',
        'maps_url',
        'days'
    ]
    df = df[cols]
    df = df.sort_values(by=['city', 'days']).reset_index(drop=True)
    df = df.groupby('city').head(20)
    df = df.rename(columns={'alias':'type', 'energy_class':'energy', 'build_year':'built'})

    return df


def add_days_ago(df, from_col, column_name):
    now_days = pd.to_datetime(datetime.datetime.now())
    created_days = pd.to_datetime(df[from_col], format='%Y-%m-%dT%H:%M:%S.%fZ')
    time_delta = now_days - created_days
    time_delta_as_days = round(time_delta / np.timedelta64(1, "D"))
    df[column_name] = time_delta_as_days.astype(int)
    return df


def fix_pricing(price):
    if pd.isna(price):
        return '-'
    price = int(price)
    price = '{:,}'.format(price)
    price = price.replace(',', '.')
    return str(price)


def add_boliga_url(estate_id):
    if str(estate_id) == '0':
        return ''
    return f'https://www.boliga.dk/bolig/{estate_id}'


if __name__ == "__main__":
    df_forsale = prepare_forsale()
    df_sold = prepare_sold()
    html_forsale = get_html_df(df_forsale, 'For Sale Estates')
    html_sold = get_html_df(df_sold, 'Sold Estates')
    email_body = '<br><br>'.join([html_forsale, html_sold])
    send_email(email_body)
