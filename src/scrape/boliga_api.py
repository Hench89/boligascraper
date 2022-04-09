import requests
import urllib
import math


FORSALE_API = 'https://api.boliga.dk/api/v2/search/results'
SOLD_API = 'https://api.boliga.dk/api/v2/sold/search/results'
ESTATE_API = 'https://api.boliga.dk/api/v2/estate/'
API_ENDPOINTS = {'forsale': FORSALE_API, 'sold': SOLD_API, 'estate': ESTATE_API}


def get_list_results(zipcode, api_name):
    api_endpoint = API_ENDPOINTS[api_name]
    total_count = _get_list_stats(zipcode, api_endpoint)
    api_calls = _get_api_calls_to_make(api_endpoint, zipcode, total_count)

    results = []
    for api_call in api_calls:
        json_data = requests.get(api_call).json()
        results += json_data['results']
    return results


def get_estate_data(estate_id):
    api_call = f'{ESTATE_API}{estate_id}'
    json_response = requests.get(api_call).json()
    return json_response


def _get_list_stats(zipcode, api_endpoint):
    api_call = f'{api_endpoint}?page=1&zipcodeFrom={zipcode}&zipcodeTo={zipcode}'
    json_data = requests.get(api_call).json()
    total_count = json_data['meta']['totalCount']
    return total_count


def _get_api_calls_to_make(api_endpoint, zipcode, total_count):
    num_calls = math.ceil(total_count / 500)
    urls_to_call = []
    for p in range(1, num_calls+1):
        url_params = {'page': p, 'pagesize': 500, 'zipcodeFrom': zipcode, 'zipcodeTo': zipcode}
        api_call = _get_url_with_params(api_endpoint, url_params)
        urls_to_call.append(api_call)
    return urls_to_call


def _get_url_with_params(endpoint, params):
    params_encoded = urllib.parse.urlencode(params)
    return f'{endpoint}?{params_encoded}'
