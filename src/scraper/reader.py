import pandas as pd
import numpy as np
import csv
from scraper.boliga import get_bolig_list, read_bolig
from scraper.helper import BoligaHelper

def compute(archive_path: str, zipcodes_path: str, stations_path: str) -> pd.DataFrame:

    bh = BoligaHelper(stations_path)

    print("step %s: reading archive and new listings" % 1)
    df_archive, df_listings = _get_whats_new(archive_path, zipcodes_path, bh)

    print("step %s: identifying differences" % 2)
    df_archive, df_add = _make_update_plan(df_archive, df_listings)

    print("step %s: updating archive" % 3)
    df = _run_updates(df_archive, df_add, bh)

    return df


def _get_whats_new(archive_path: str, zipcodes_path: str, bh: BoligaHelper):

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


def _run_updates(df_archive, df_add, bh: BoligaHelper):

    # process items
    if len(df_add) > 0:
        items_to_process = df_add[['boliga_id', 'zipcode']].to_numpy()
        df_add = read_bolig(items_to_process, bh)

    # merged df
    try:
        if df_archive is None:
            df = df_add
        else:
            df = pd.concat([df_archive, df_add]).reset_index(drop=True)
    except ValueError:
        df = df_archive

    # remove duplicates
    df = df.groupby(['boliga_id']).head(1)

    # date related data
    df['market_days'] = df.apply(lambda x: bh.days_on_market(x.created_date), axis=1)
    df = df.sort_values(by=['market_days', 'list_price']).reset_index(drop=True)

    return df
