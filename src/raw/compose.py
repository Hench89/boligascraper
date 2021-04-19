
from .list import extract_list
from .estate import extract_estate
import traceback
import sys

def compose(root_path, zipcodes_path):

    print(f'===== RAW =====')

    for_sale_list_path =  f'{root_path}/raw/forsale/list'
    sold_list_path = f'{root_path}/raw/sold/list'
    for_sale_estate_path = f'{root_path}/raw/forsale/estate'
    sold_estate_path = f'{root_path}/raw/sold/estate'

    # process for sale data
    extract_list(for_sale_list_path, 'for sale', zipcodes_path)
    extract_estate(for_sale_list_path, for_sale_estate_path, 'for sale', zipcodes_path)

    # process sold data
    extract_list(sold_list_path, 'sold', zipcodes_path)
    extract_estate(sold_list_path, sold_estate_path, 'sold', zipcodes_path)
