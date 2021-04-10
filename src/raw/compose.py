
from .list import extract_list
from .estate import extract_estate
import traceback
import sys

def compose(archive_root, zipcodes):
    try:
        paths = get_path_dict(archive_root)
        for fetch_type in paths.keys():
            print(f'===== {fetch_type.upper()} =====')

            print('Fetching data from list..')
            list_url = paths[fetch_type]['list']
            extract_list(list_url, fetch_type, zipcodes = zipcodes)

            print('Fetching estate data..')
            estate_url = paths[fetch_type]['estate']
            extract_estate(list_url, estate_url, fetch_type, zipcodes=zipcodes)
    except:
        traceback.print_exc()
        sys.exit()
    print('RAW UP TO DATE!')


def get_path_dict(root_path):
    dict = {
        'for sale': {
            'list' : f'{root_path}/raw/forsale/list', 
            'estate': f'{root_path}/raw/forsale/estate'
        },
        'sold': {
            'list' : f'{root_path}/raw/sold/list', 
            'estate': f'{root_path}/raw/sold/estate'
        }
    }
    return dict
