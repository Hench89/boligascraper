import pandas as pd
from raw import compose
import traceback
import sys


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

archive_root = './archive'
compose(archive_root, zipcodes)
