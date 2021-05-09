import requests
import math


def get_pages(zipcode: str, api: str):
    if api == 'forsale':
        url = construct_sold_api_url(page=1, zipcode=zipcode)
    if api == 'sold':
        url = construct_for_sale_api_url(page=1, zipcode=zipcode)
    data = read_json_from_url(url)
    total_count = data['meta']['totalCount']
    api_calls_required = math.ceil(total_count / 500)
    return api_calls_required


def construct_sold_api_url(page = None, pagesize = None, zipcode = None):
    api_end_point = "https://api.boliga.dk/api/v2/sold/search/results?"
    parameters = []
    parameters += [f'page={page}'] if page is not None else []
    parameters += [f'pagesize={pagesize}'] if pagesize is not None else []
    parameters += [f'zipcodeFrom={zipcode}'] if zipcode is not None else []
    parameters += [f'zipcodeTo={zipcode}'] if zipcode is not None else []
    return api_end_point + '&'.join(parameters)


def construct_for_sale_api_url(page = None, pagesize = None, zipcode = None):
    api_endpoint = "https://api.boliga.dk/api/v2/search/results?"
    parameters = []
    parameters += [f'page={page}'] if page is not None else []
    parameters += [f'pagesize={pagesize}'] if pagesize is not None else []
    parameters += [f'zipcodeFrom={zipcode}'] if zipcode is not None else []
    parameters += [f'zipcodeTo={zipcode}'] if zipcode is not None else []
    return api_end_point + '&'.join(parameters)


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

def read_json_from_url(url):
    return requests.get(url).json()
