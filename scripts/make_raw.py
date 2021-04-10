import pandas as pd
from raw import extract_list, extract_estate
import traceback
import sys


# load zipcodes
try:
    zipcodes_path = './static/zipcode.csv'
    zipcodes = pd.read_csv(zipcodes_path, usecols = [0]).iloc[:,0]
    if len(zipcodes) == 0:
        print('Failed to load zipcodes!')
        sys.exit()
    print(f'Loaded {len(zipcodes)} zipcode(s)')
except:
    print(f'Could not load zipcodes from {zipcodes_path}')
    traceback.print_exc()
    sys.exit()

# setup archive paths
archive_path = './archive'
paths = {
    'for sale': {
        'list' : f'{archive_path}/raw/forsale/list', 
        'estate': f'{archive_path}/raw/forsale/estate'
    },
    'sold': {
        'list' : f'{archive_path}/raw/sold/list', 
        'estate': f'{archive_path}/raw/sold/estate'
    }
}


for fetch_type in paths.keys():

    print(f'===== {fetch_type.upper()} DATA =====')
    list_url = paths[fetch_type]['list']
    estate_url = paths[fetch_type]['estate']

    try:
        print('Fetching data from list..')
        extract_list(list_url, fetch_type, zipcodes = zipcodes)
    except:
        print('Could not fetch batch data')
        traceback.print_exc()
        sys.exit()

    try:
        print('Fetching estate data..')
        extract_estate(list_url, estate_url, fetch_type, zipcodes=zipcodes)
    except:
        print('Could not fetch estate data!')
        traceback.print_exc()
        sys.exit()

print('Done!')
