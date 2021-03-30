import pandas as pd
import numpy as np
import csv
from scraper.boliga import get_listings_from_list, get_bolig_from_list
from dfutils.geo import get_dk_lat_lng, get_nearest_station
from dfutils.dates import days_on_market

def compute(archive_path, zipcodes_path, stations_path):

    # read archive
    print("step %s: reading archive" % 1)
    try:
        df_archive = pd.read_csv(archive_path, quoting=csv.QUOTE_NONNUMERIC)
        print('.. read %s listings from archive:' % len(df_archive))
    except Exception as e:
        df_archive = None
        print('.. starting a new archive')

    # read new items
    print("step %s: reading current listings" % 2)
    df_zip = pd.read_csv(zipcodes_path)
    zipcode_list = df_zip[df_zip.columns[0]]
    listings = get_listings_from_list(zipcode_list)

    print("step %s: identifying differences" % 3)
    updated_archive, new_items = _make_update_plan(df_archive, listings)

    print("step %s: updating archive" % 4)
    df_stations = pd.read_csv(stations_path, sep=',')
    df = _run_updates(updated_archive, new_items, df_stations)

    return df



def _make_update_plan(df_archive, listings):

    # if no archive, return only new items
    if df_archive is None:
        print('.. items to process: %s' % (len(listings)))
        return None, np.int64(listings)

    # conversion
    listings = np.int64(listings)
    archive = np.int64(df_archive['boliga_id'])

    # ids to remove and insert
    seta = set(listings)
    setb = set(archive)
    set_rem = setb.difference(seta)
    set_add = seta.difference(setb)

    print('.. new items to process: %s' % (len(set_add)))
    print('.. items to remove from archive: %s' % len(set_rem))

    # update
    updated_archive = df_archive[~df_archive['boliga_id'].isin(set_rem)].reset_index(drop=True)
    new_items = list(set_add)

    return updated_archive, new_items


def _run_updates(updated_archive, new_items, df_stations):

    is_items_to_process = True if len(new_items) > 0 else False
    is_empty_archive = True if updated_archive is None else False

    # no archive and nothing to process
    if is_empty_archive and not is_items_to_process:
        return None

    # nothing to process
    elif not is_items_to_process:
        df = updated_archive

    else:

        # fetch new data
        df_processed = get_bolig_from_list(new_items)

        # enrich with geo related columns
        print(".. adding geo related information to listings")
        df_processed['latlng'] = df_processed.apply(lambda x: get_dk_lat_lng(x.address), axis=1)
        df_processed['gmaps'] = df_processed['latlng'].apply(lambda x: 'https://maps.google.com/?q=' + str(x))
        df_processed['station_dist_km'] = df_processed.apply(lambda x: get_nearest_station(df_stations, x.latlng), axis=1)

        # merge with archive
        if is_empty_archive:
            df = df_processed
        else:
            df = pd.concat([updated_archive, df_processed]).reset_index(drop=True)

    # remove duplicates
    df = df.groupby(['boliga_id']).head(1)

    # set market_days again
    df['market_days'] = df.apply(lambda x: days_on_market(x.created_date), axis=1)

    # reorder merged list
    df = df.sort_values(by=['market_days', 'list_price']).reset_index(drop=True)

    
    return df
