import pandas as pd
from raw import extract_sold, extract_estate
import traceback
import sys


print('===== Getting Started =====')
zipcodes_path = './static/zipcode.csv'
archive_path = './archive'
sold_archive_path = f'{archive_path}/raw/sold'
estate_archive_path = f'{archive_path}/raw/estate'

try:
    zipcodes = pd.read_csv(zipcodes_path, usecols = [0]).iloc[:,0]
    print(f'Loaded {len(zipcodes)} zipcode(s) and set prepared archive here: {archive_path}')
except:
    print(f'Could not load zipcodes from {zipcodes_path}')
    traceback.print_exc()
    sys.exit()


print('===== Fetching latest sold batch =====')
try:    
    extract_sold(sold_archive_path, zipcodes = zipcodes)
except:
    print(f'Could not fetch sold batch data')
    traceback.print_exc()
    sys.exit()


try:
    print('===== Fetching (new) estate data =====')
    extract_estate(estate_archive_path, sold_archive_path=sold_archive_path, zipcodes=zipcodes)
except:
    print(f'Could not fetch estate data')
    traceback.print_exc()
    sys.exit()

print('Done!')
