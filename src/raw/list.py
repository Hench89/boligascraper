from json import dumps
from .utils import compress_save, read_json_from_url, get_latest_file, file_age_hours
from math import ceil
from datetime import datetime


def extract_list(folder_path, api_endpoint, zipcodes = []):

    if len(zipcodes)==0:
        return print('No zipcodes to process!')

    # get latest batch file
    latest_batch_file = get_latest_file(folder_path)
    if latest_batch_file is None:
        print('Fetching batch for the first time')
        fetch_list_data(folder_path, zipcodes, api_endpoint)
        return

    # determine age of file
    batch_age = file_age_hours(latest_batch_file)
    if batch_age < 20:
        print(f'Batch file is only {batch_age} hours old. Will reuse it for 20 hours')
        return
    else:
        print(f'Latest batch is {batch_age} hours old. Fetching new one!')
        fetch_list_data(folder_path, zipcodes, api_endpoint)


def fetch_list_data(folder_path, zipcodes, api_endpoint):

    if not api_endpoint in ['for sale', 'sold']:
        print('did not specify a known fetch type')
        return None

    # fetch sold data
    sold_estate_list = []
    for z in zipcodes:
        sold_estate_list += get_sold_data(z, api_endpoint)
    sold_estates_json = dumps(sold_estate_list)

    # save sold data
    time_str = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    file_path = f'{folder_path}/{time_str}.zlib'
    compress_save(file_path, sold_estates_json)


def get_sold_data(zipcode, api_endpoint):

    def get_api_url(api_endpoint, page = None, pagesize = None, zipcode = None):

        sold_api_endpoint = "https://api.boliga.dk/api/v2/sold/search/results?"
        for_sale_api_endpoint = "https://api.boliga.dk/api/v2/search/results?"
        api_end_point = sold_api_endpoint if api_endpoint == 'sold' else for_sale_api_endpoint

        parameters = []
        parameters += [f'page={page}'] if page is not None else []
        parameters += [f'pagesize={pagesize}'] if pagesize is not None else []
        parameters += [f'zipcodeFrom={zipcode}'] if zipcode is not None else []
        parameters += [f'zipcodeTo={zipcode}'] if zipcode is not None else []
        return api_end_point + '&'.join(parameters)

    # how much to process
    url = get_api_url(api_endpoint, page=1, zipcode=zipcode)
    data = read_json_from_url(url)
    total_count = data['meta']['totalCount']
    to_process = ceil(total_count / 500)

    # fetch data
    estate_list = []
    for p in range(1, to_process+1):
        url = get_api_url(api_endpoint, page=p, pagesize=500, zipcode=zipcode)
        data = read_json_from_url(url)
        print(f'Fetching list data from "{api_endpoint}" endpoint - {zipcode} with {total_count} records (page {p} of {to_process})')
        estate_list += [estate for estate in data['results']]

    return estate_list
