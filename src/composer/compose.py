import pandas as pd
import numpy as np
from os import path
from boliga import get_listings_from_list, get_bolig_from_list
from utils import days_on_market, compare_number_sets


def wrap_compose(zipcodes_path, stations_path, archive_path):
    
    if not path.exists(zipcodes_path):
        return print('no zipcodes to use')
    zipcodes = pd.read_csv(zipcodes_path, usecols = [0]).iloc[:,0]

    archive = []
    if path.exists(archive_path):
        archive = pd.read_csv(archive_path).to_dict(orient='records')
    
    stations = []
    if path.exists(stations_path):
        stations = pd.read_csv(stations_path).to_dict(orient='records')
    
    return compose(zipcodes, archive, stations)


def compose(zipcodes, archive, stations):

    # get ids of new listings
    new_ids = get_listings_from_list(zipcodes)
    new_ids.append(1753899)
    print(".. total listings: %s" % (len(new_ids)))

    # compare against archive
    print("Comparing listings against archive")
    archive_ids = [d['boliga_id'] for d in archive]
    new_ids, unchanged_ids, archive_ids = compare_number_sets(new_ids, archive_ids)
    print('.. new items to process: %s' % len(new_ids))
    print('.. unchanged items: %s' % (len(unchanged_ids)))
    print('.. items to remove from archive: %s' % len(archive_ids))
    
    # items to re-process, because sold
    sold_ids = []
    if len(archive) > 0 and len(archive_ids) > 0:
        for i, item in enumerate(archive):
            if item['boliga_id'] in archive_ids:
                sold_ids.append(item['boliga_id'])
                del archive[i]
        print('.. items to reprocess: %s' % len(sold_ids))
    
    reprocess_ids = list(set(new_ids) - set(sold_ids))
    
    # process new items
    if len(reprocess_ids) > 0:
        print('Processing new items')
        bolig_list = get_bolig_from_list(reprocess_ids, stations)
        for b in bolig_list:
            archive.append(b)

    # update market days
    if len(archive) > 0:
        for item in archive:
            item['market_days'] = days_on_market(item['created_date'])

    if len(archive) == 0:
        return None

    # finalize as dataframe
    df = pd.DataFrame(archive).sort_values(by=['market_days'])
    return df
