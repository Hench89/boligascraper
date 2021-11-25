import requests, math, urllib


forsale_api = 'https://api.boliga.dk/api/v2/search/results'
sold_api = 'https://api.boliga.dk/api/v2/sold/search/results'
estate_api = 'https://api.boliga.dk/api/v2/estate/'


def get_forsale_results(zipcode) -> list:
    total_count = get_list_stats(zipcode, forsale_api)
    api_calls = get_api_calls_to_make(forsale_api, zipcode, total_count)
    results = []
    for api_call in api_calls:
        json_data = requests.get(api_call).json()
        results += json_data['results']
    return results


def get_sold_results(zipcode) -> list:
    total_count = get_list_stats(zipcode, sold_api)
    api_calls = get_api_calls_to_make(sold_api, zipcode, total_count)
    results = []
    for api_call in api_calls:
        json_data = requests.get(api_call).json()
        results += json_data['results']
    return results


def get_list_stats(zipcode, api_endpoint) -> int:
    api_call = f'{api_endpoint}?page=1&zipcodeFrom={zipcode}&zipcodeTo={zipcode}'
    json_data = requests.get(api_call).json()
    total_count = json_data['meta']['totalCount']
    return total_count


def get_estate_data(estate_id) -> dict:
    api_call = f'{estate_api}{estate_id}'
    json_response = requests.get(api_call).json()
    return json_response


def get_api_calls_to_make(api_endpoint, zipcode, total_count) -> list:
    num_calls = get_api_calls_required(total_count)
    urls_to_call = []
    for p in range(1, num_calls+1):
        url_params = {'page': p, 'pagesize': 500, 'zipcodeFrom': zipcode, 'zipcodeTo': zipcode}
        api_call = get_url_with_params(api_endpoint, url_params)
        urls_to_call.append(api_call)
    return urls_to_call


def get_url_with_params(endpoint: str, params: dict) -> str:
    params_encoded = urllib.parse.urlencode(params)
    return f'{endpoint}?{params_encoded}'


def get_api_calls_required(total_count: int):
    return math.ceil(total_count / 500)
