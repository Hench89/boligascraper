from json import dumps
from .utils import compress_save, read_json_from_url, get_latest_file, file_age_hours
from math import ceil
#from time import gmtime, strftime, strptime
from datetime import datetime
from os import path

def run(archive_path, zipcodes = []):

    if len(zipcodes)==0:
        return print('No zipcodes to process!')
    
    # get latest batch file
    latest_batch_file = get_latest_file(archive_path)
    if latest_batch_file is None:
        print('Fetching batch for the first time')
        fetch_sold_data(archive_path, zipcodes)
        return
    
    # determine age of file
    batch_age = file_age_hours(latest_batch_file)
    if batch_age < 20:
        print(f'Batch file is only {batch_age} hours old. Will reuse it for 20 hours')
        return
    else:
        print(f'Latest batch is {batch_age} old. Fetching new one!')
        fetch_sold_data(archive_path, zipcodes)


def fetch_sold_data(archive_path, zipcodes):

    # fetch sold data
    sold_estate_list = []
    for z in zipcodes:
        sold_estate_list += get_sold_data(z)
    sold_estates_json = dumps(sold_estate_list)

    # save sold data
    time_str = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    file_path = f'{archive_path}/{time_str}.zlib'
    compress_save(file_path, sold_estates_json)


def get_sold_data(zipcode):

    def get_sold_url(page = None, pagesize = None, zipcode = None):
        parameters = []
        parameters += [f'page={page}'] if page is not None else []
        parameters += [f'pagesize={pagesize}'] if pagesize is not None else []
        parameters += [f'zipcodeFrom={zipcode}'] if zipcode is not None else []
        parameters += [f'zipcodeTo={zipcode}'] if zipcode is not None else []
        return "https://api.boliga.dk/api/v2/sold/search/results?" + '&'.join(parameters)

    # how much to process
    url = get_sold_url(page=1, pagesize=1, zipcode=zipcode)
    data = read_json_from_url(url)
    total_count = data['meta']['totalCount']
    to_process = ceil(total_count / 500)

    # fetch data
    estate_list = []
    for p in range(1, to_process+1):
        url = get_sold_url(page=p, pagesize=500, zipcode=zipcode)
        data = read_json_from_url(url)
        cfrom = data['meta']['countFrom']
        cto = data['meta']['countTo']
        print(f'fetching data in {zipcode} from record {cfrom} to {cto} (page {p} of {to_process})')
        estate_list += [estate for estate in data['results']]

    return estate_list
