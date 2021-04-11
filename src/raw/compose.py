
from .list import extract_list
from .estate import extract_estate
import traceback
import sys

def compose(archive_root, zipcodes):
    try:
        paths = get_api_dict(archive_root)
        for api_endpoint in paths.keys():
            print(f'===== {api_endpoint.upper()} RAW =====')

            print('Fetching data from list..')
            list_url = paths[api_endpoint]['list']
            extract_list(list_url, api_endpoint, zipcodes = zipcodes)

            print('Fetching estate data..')
            estate_url = paths[api_endpoint]['estate']
            extract_estate(list_url, estate_url, api_endpoint, zipcodes=zipcodes)
    except:
        traceback.print_exc()
        sys.exit()
    print('RAW UP TO DATE!')


def get_api_dict(root_path):
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
