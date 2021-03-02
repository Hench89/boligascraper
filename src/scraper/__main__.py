import pandas as pd
import numpy as np
import csv
import os
from scraper import reader as br
from scraper import cleaner as cln
from scraper import helper as hlp

def read_data():

    # read from archive
    try:
        df_archive = pd.read_csv('./output/boliga.csv', quoting=csv.QUOTE_NONNUMERIC)
        print('.. read %s listings from archive:' % len(df_archive))
    except FileNotFoundError:
        df_archive = pd.DataFrame(columns=cln.clean_cols)
        print('.. starting a new archive')

    # read from boliga
    print('.. fetching all listings from boliga')
    df_listings = br.get_boliga_listings()

    return df_archive, df_listings

def diff_data(df_archive, df_listings):

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

def process_listings(df_archive, df_add):

    # process items
    if len(df_add) > 0:
        items_to_process = df_add[['boliga_id', 'zipcode']].to_numpy()
        df_add = br.get_boliga_data(items_to_process)

    # merged df
    try:
        df = pd.concat([df_archive, df_add]).reset_index(drop=True)
    except ValueError:
        df = df_archive

    # remove duplicates
    df = df.groupby(['boliga_id']).head(1)

    # date related data
    df['market_days'] = df.apply(lambda x: hlp.days_on_market(x.created_date), axis=1)
    df = df.sort_values(by=['market_days', 'list_price']).reset_index(drop=True)
    df = df[cln.print_cols]

    return df

def save_data(df, csv_path):
    if not os.path.exists(os.path.dirname(csv_path)):
        try:
            os.makedirs(os.path.dirname(csv_path))
        except OSError:
            raise
    df.to_csv(csv_path, index=False, quoting=csv.QUOTE_NONNUMERIC)


# read from archive
print("step %s: reading archive and new listings" % 1)
df_archive, df_listings = read_data()

# identify differences
print("step %s: identifying differences" % 2)
df_archive, df_add = diff_data(df_archive, df_listings)

# process new things
print("step %s: updating archive" % 3)
df = process_listings(df_archive, df_add)

# save csv
print("step %s: storing archive" % 4)
csv_path = './output/boliga.csv'
save_data(df, csv_path)
