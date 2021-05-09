import requests
import math


def get_api_endpoint(api_name: str):
    d = {
        'forsale' : 'https://api.boliga.dk/api/v2/search/results',
        'sold' : 'https://api.boliga.dk/api/v2/sold/search/results'
    }
    api_endpoint = d[api_name]
    return api_endpoint


def add_parameters(api_endpoint:str, page = None, pagesize = None, zipcode = None):
    parameters = []
    parameters += [f'page={page}'] if page is not None else []
    parameters += [f'pagesize={pagesize}'] if pagesize is not None else []
    parameters += [f'zipcodeFrom={zipcode}'] if zipcode is not None else []
    parameters += [f'zipcodeTo={zipcode}'] if zipcode is not None else []
    joined_params = '&'.join(parameters)
    return f'{api_endpoint}?{joined_params}'


def get_api_pages_for_zipcode(api_name: str, zipcode: str):
    api_endpoint = get_api_endpoint(api_name)
    url = add_parameters(api_endpoint, page=1, zipcode=zipcode)
    data = read_json_from_url(url)
    total_count = data['meta']['totalCount']
    api_calls_required = math.ceil(total_count / 500)
    return api_calls_required


def get_list_data_from_zipcodes(api_name: str, zipcodes: list):
    return [get_list_data_from_zipcode(api_name, z) for z in zipcodes]


def get_list_data_from_zipcode(api_name: str, zipcode: str):
    n = get_api_pages_for_zipcode(api_name, zipcode)
    api_endpoint = get_api_endpoint(api_name)
    list_data = []
    for p in range(1, n+1):
        url = add_parameters(api_endpoint, page=p, pagesize=500, zipcode=zipcode)
        data = read_json_from_url(url)
        results = data['results']
        print(f'Fetching list data from "{api_endpoint}" endpoint - {zipcode} with (page {p} of {n})')
        list_data += [i for i in results]
    return list_data




def read_json_from_url(url):
    return requests.get(url).json()
