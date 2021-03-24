import pandas as pd
import numpy as np
import csv
from scraper.boliga import get_bolig_list, read_bolig
from geo.geo import StationDist, get_dk_lat_lng
from datetime import datetime, date
import re


def compute(archive_path: str, zipcodes_path: str, stations_path: str) -> pd.DataFrame:

    print("step %s: reading archive and new listings" % 1)
    df_archive, df_listings = _get_whats_new(archive_path, zipcodes_path)

    print("step %s: identifying differences" % 2)
    df_archive, df_add = _make_update_plan(df_archive, df_listings)

    print("step %s: updating archive" % 3)
    df = _run_updates(df_archive, df_add, stations_path)

    return df


def _get_whats_new(archive_path: str, zipcodes_path: str):

    # read from archive
    try:
        df_archive = pd.read_csv(archive_path, quoting=csv.QUOTE_NONNUMERIC)
        print('.. read %s listings from archive:' % len(df_archive))
    except FileNotFoundError:
        df_archive = None
        print('.. starting a new archive')

    # read from boliga
    print('.. fetching all listings from boliga')
    df_zip = pd.read_csv(zipcodes_path, sep=',')
    df_listings = get_bolig_list(df_zip)

    return df_archive, df_listings


def _make_update_plan(df_archive: pd.DataFrame, df_listings: pd.DataFrame) -> pd.DataFrame:

    # if no archive, return only new items
    if df_archive is None:
        print('.. items to process: %s' % (len(df_listings)))
        df_listings['boliga_id'] = np.int64(df_listings['boliga_id'])
        df_add = df_listings
        return df_archive, df_add

    # conversion
    df_listings['boliga_id'] = np.int64(df_listings['boliga_id'])
    df_archive['boliga_id'] = np.int64(df_archive['boliga_id'])

    # ids to remove and insert
    seta = set(df_listings['boliga_id'])
    setb = set(df_archive['boliga_id'])
    set_rem = setb.difference(seta)
    set_add = seta.difference(setb)

    print('.. new items to process: %s' % (len(set_add)))
    print('.. items to remove from archive: %s' % len(set_rem))

    # remove from old, a
    df_archive = df_archive[~df_archive['boliga_id'].isin(set_rem)].reset_index(drop=True)
    df_add = df_listings[df_listings['boliga_id'].isin(set_add)].reset_index(drop=True)

    return df_archive, df_add


def _run_updates(df_archive, df_add, stations_path):

    # process items
    if len(df_add) > 0:
        items_to_process = df_add[['boliga_id', 'zipcode']].to_numpy()
        df_raw = read_bolig(items_to_process)
        df_fancy = _make_fancy(df_raw, stations_path)

    # create merged df
    try:
        if df_archive is None:
            df = df_add
        else:
            df = pd.concat([df_archive, df_add]).reset_index(drop=True)
    except ValueError:
        df = df_archive

    # remove duplicates
    df = df.groupby(['boliga_id']).head(1)

    # reorder merged list
    df = df.sort_values(by=['market_days', 'list_price']).reset_index(drop=True)

    return df


def _make_fancy(df, stations_path):

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

    # cleaning of created date
    def date_clean(date_string):
        date_string = date_string.replace('Oprettet ', '').replace('.', '')
        date_value = datetime.strptime(date_string, '%d %b %Y')
        return date_value
    df['created_date'] = df['created_date'].apply(lambda x: date_clean(x))

    # geo related data
    sd = StationDist(stations_path)
    df['latlng'] = df['address1'].apply(lambda x: get_dk_lat_lng(x))
    df['gmaps'] = df['latlng'].apply(lambda x: 'https://maps.google.com/?q=' + str(x))
    df['station_dist_km'] = df.apply(lambda x: sd.get_dist_to_station(x.zipcode, x.latlng), axis=1)

    # set days on market
    def days_on_market(created_date_string):
        try:
            today_date = date.today()
            created_date_string = str(created_date_string)[:10]
            created_date = datetime.strptime(created_date_string, '%Y-%m-%d').date()
            return (today_date - created_date).days
        except ValueError:
            return ''
    df['market_days'] = df.apply(lambda x: days_on_market(x.created_date), axis=1)

    # cleaned columns
    clean_cols = ['boliga_id', 'address1', 'address2', 'zipcode', 'list_price', 'living_area', 
        'lot_area', 'rooms', 'floors', 'construction_date', 'energy_rating',
        'taxes_pr_month', 'bsmnt_area', 'station_dist_km', 'created_date', 'url', 'gmaps']
    df = df[clean_cols]

    return df
