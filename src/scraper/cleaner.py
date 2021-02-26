import re
from datetime import datetime

clean_cols = ['boliga_id', 'address1', 'address2', 'zipcode', 'list_price', 'living_area',
              'lot_area', 'rooms', 'floors', 'construction_date', 'energy_rating',
              'taxes_pr_month', 'bsmnt_area', 'station_dist_km', 'created_date', 'url', 'gmaps']

print_cols = ['boliga_id', 'address1', 'address2', 'zipcode', 'list_price',
              'living_area', 'lot_area', 'rooms', 'floors', 'construction_date', 'energy_rating',
              'taxes_pr_month', 'bsmnt_area', 'station_dist_km', 'created_date', 'market_days', 'url',
              'gmaps']

def clean_boliga_data(df):

    # rename some columns
    df = df.rename(
        columns={
            '#icon-square': 'living_area',
            '#icon-lot-size': 'lot_area',
            '#icon-rooms': 'rooms',
            '#icon-floor': 'floors',
            '#icon-construction-year': 'construction_date',
            '#icon-energy': 'energy_rating',
            '#icon-taxes': 'taxes_pr_month',
            '#icon-basement-size': 'bsmnt_area',

        }
    )

    # split address
    df['address1'] = df['address'].apply(lambda x: x.split(',')[0])
    df['address2'] = df['address'].apply(lambda x: x.split(',')[1])
    df = df.drop(columns=['address'])

    # numerical columns
    trim = re.compile(r'[^\d]+')
    df['list_price'] = df['list_price'].apply(lambda x: trim.sub('', x))
    df['living_area'] = df['living_area'].apply(lambda x: trim.sub('', x))
    df['lot_area'] = df['lot_area'].apply(lambda x: trim.sub('', x))
    df['floors'] = df['floors'].apply(lambda x: trim.sub('', x))
    df['taxes_pr_month'] = df['taxes_pr_month'].apply(lambda x: trim.sub('', x))
    df['bsmnt_area'] = df['bsmnt_area'].apply(lambda x: trim.sub('', x))

    # created date
    df['created_date'] = df['created_date'].apply(lambda x: _date_clean(x))

    return df


def _date_clean(x):
    x = x.replace('Oprettet ', '').replace('.', '')
    date_value = datetime.strptime(x, '%d %b %Y')
    return date_value
