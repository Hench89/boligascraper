from json import dumps
from .utils import compress_save, read_json_from_url, get_latest_file, file_age_hours
from math import ceil
from datetime import datetime


def extract_list(folder_path, fetch_type, zipcodes = []):

    if len(zipcodes)==0:
        return print('No zipcodes to process!')
    
    # get latest batch file
    latest_batch_file = get_latest_file(folder_path)
    if latest_batch_file is None:
        print('Fetching batch for the first time')
        fetch_list_data(folder_path, zipcodes, fetch_type)
        return
    
    # determine age of file
    batch_age = file_age_hours(latest_batch_file)
    if batch_age < 20:
        print(f'Batch file is only {batch_age} hours old. Will reuse it for 20 hours')
        return
    else:
        print(f'Latest batch is {batch_age} old. Fetching new one!')
        fetch_list_data(folder_path, zipcodes, fetch_type)


def fetch_list_data(folder_path, zipcodes, fetch_type):

    if not fetch_type in ['for sale', 'sold']:
        print('did not specify a known fetch type')
        return None
    
    # fetch sold data
    sold_estate_list = []
    for z in zipcodes:
        sold_estate_list += get_sold_data(z, fetch_type)
    sold_estates_json = dumps(sold_estate_list)

    # save sold data
    time_str = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    file_path = f'{folder_path}/{time_str}.zlib'
    compress_save(file_path, sold_estates_json)


def get_sold_data(zipcode, fetch_type):

    def get_sold_url(page = None, pagesize = None, zipcode = None):
        parameters = []
        parameters += [f'page={page}'] if page is not None else []
        parameters += [f'pagesize={pagesize}'] if pagesize is not None else []
        parameters += [f'zipcodeFrom={zipcode}'] if zipcode is not None else []
        parameters += [f'zipcodeTo={zipcode}'] if zipcode is not None else []
        return "https://api.boliga.dk/api/v2/sold/search/results?" + '&'.join(parameters)

    def get_for_sale_url(page = None, pagesize = None, zipcode = None):
        parameters = []
        parameters += [f'page={page}'] if page is not None else []
        parameters += [f'pagesize={pagesize}'] if pagesize is not None else []
        parameters += [f'zipcodeFrom={zipcode}'] if zipcode is not None else []
        parameters += [f'zipcodeTo={zipcode}'] if zipcode is not None else []
        return "https://api.boliga.dk/api/v2/search/results?" + '&'.join(parameters)

    # how much to process
    get_url = get_sold_url if fetch_type == 'sold' else get_for_sale_url
    url = get_url(page=1, zipcode=zipcode)
    data = read_json_from_url(url)
    total_count = data['meta']['totalCount']
    to_process = ceil(total_count / 500)

    # fetch data
    estate_list = []
    for p in range(1, to_process+1):
        url = get_url(page=p, pagesize=500, zipcode=zipcode)
        data = read_json_from_url(url)
        print(f'fetching "{fetch_type}" data in {zipcode} with {total_count} records (page {p} of {to_process})')
        estate_list += [estate for estate in data['results']]

    return estate_list
