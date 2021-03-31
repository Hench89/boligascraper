import pandas as pd
import csv
from pathlib import Path
from boliga import get_listings_from_list, get_bolig_from_list
from utils import get_dk_lat_lng, get_nearest_station, days_on_market, compare_number_sets

def wrap_compose(zipcodes_path, stations_path : None, archive_path : None):

    # load zipcodes
    df_zip = pd.read_csv(zipcodes_path)
    zipcodes = df_zip[df_zip.columns[0]]

    # load archive and stations
    def try_load_file(filepath):
        if Path(filepath).exists():
            return pd.read_csv(filepath, quoting=csv.QUOTE_NONNUMERIC)
        return None
    
    df_archive = try_load_file(archive_path)
    df_stations = try_load_file(stations_path)

    return compose(zipcodes, df_archive, df_stations)


def compose(zipcodes, df_archive, df_stations):

    # archive summary
    print("step %s: reading archive" % 1)
    if df_archive is None:
        print('.. starting a new archive')
    else:
        print('.. read %s listings from archive:' % len(df_archive))

    # read new items
    print("step %s: reading current listings" % 2)
    current_listings = get_listings_from_list(zipcodes)
    print(".. found %s total listings" % (len(current_listings)))

    # when there is not archive
    if df_archive is None:
        print('.. new items to process: %s' % (len(current_listings)))
        print("step %s: updating archive" % 3)
        return _run_updates(current_listings, df_stations = df_stations)

    else:
        # identify how much to process
        print("step %s: identifying differences" % 3)
        archive_listings = df_archive['boliga_id'] if df_archive is not None else None
        a_only, intersection, b_only = compare_number_sets(current_listings, archive_listings)

        print('.. new items to process: %s' % (len(a_only)))
        print('.. unchanged items: %s' % (len(intersection)))
        print('.. items to remove from archive: %s' % len(b_only))

        # update
        print("step %s: updating archive" % 4)
        new_items = list(a_only)
        df_archive = df_archive[~df_archive['boliga_id'].isin(set(b_only))].reset_index(drop=True)

        if len(new_items) == 0:
            return df_archive
        return _run_updates(
            new_items = new_items,
            df_archive = df_archive,
            df_stations = df_stations
        )



def _run_updates(new_items, df_stations = None, df_archive = None):

    # fetch new data
    df_processed = get_bolig_from_list(new_items)

    # enrich with geo related columns
    print(".. adding geo related information to listings")
    df_processed['latlng'] = df_processed.apply(lambda x: get_dk_lat_lng(x.address), axis=1)
    df_processed['gmaps'] = df_processed['latlng'].apply(lambda x: 'https://maps.google.com/?q=' + str(x))
    df_processed['station_dist_km'] = df_processed.apply(lambda x: get_nearest_station(df_stations, x.latlng), axis=1)

    # merge with archive
    if df_archive is None:
        df = df_processed
    else:
        df = pd.concat([df_archive, df_processed]).reset_index(drop=True)

    # remove duplicates
    df = df.groupby(['boliga_id']).head(1)

    # set market_days again
    df['market_days'] = df.apply(lambda x: days_on_market(x.created_date), axis=1)

    # reorder merged list
    df = df.sort_values(by=['market_days', 'list_price']).reset_index(drop=True)

    return df
