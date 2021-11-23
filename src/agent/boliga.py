import requests, math, urllib
from .utils import convert_str_to_int


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
    for i in range(len(results)):
        results[i] = filter_and_rename_estate(results[i])
        results[i] = convert_types_in_estate_data(results[i])
    return results


def get_sold_results(zipcode) -> list:
    total_count = get_list_stats(zipcode, sold_api)
    api_calls = get_api_calls_to_make(sold_api, zipcode, total_count)
    results = []
    for api_call in api_calls:
        json_data = requests.get(api_call).json()
        results += json_data['results']
    for i in range(len(results)):
        results[i] = filter_and_rename_estate(results[i])
        results[i] = convert_types_in_estate_data(results[i])
    return results


def get_list_stats(zipcode, api_endpoint) -> int:
    api_call = f'{api_endpoint}?page=1&zipcodeFrom={zipcode}&zipcodeTo={zipcode}'
    json_data = requests.get(api_call).json()
    total_count = json_data['meta']['totalCount']
    return total_count


def get_estate_data(estate_id) -> dict:
    api_call = f'{estate_api}{estate_id}'
    json_response = requests.get(api_call).json()
    estate_dict = filter_and_rename_estate(json_response)
    estate_dict = convert_types_in_estate_data(estate_dict)
    return estate_dict


def filter_and_rename_estate(estate_dict) -> dict:
    rename_dict = {
        'estateUrl': 'estate_url',
        'cleanStreet': 'clean_street_name',
        'id': 'estate_id',
        'estateId': 'estate_id',
        'latitude': 'latitude',
        'longitude': 'longitude',
        'propertyType': 'property_type',
        'priceChangePercentTotal': 'price_change_pct_total',
        'energyClass': 'energy_class',
        'price': 'price',
        'rooms': 'rooms',
        'size': 'living_area_size',
        'lotSize': 'lot_size',
        'floor': 'floor',
        'buildYear': 'construction_year',
        'city': 'city',
        'isActive': 'is_active',
        'zipCode': 'zipcode',
        'street': 'street_name',
        'squaremeterPrice': 'sqm_price',
        'createdDate': 'created_date',
        'net': 'net',
        'exp': 'exp',
        'basementSize': 'basement_size'
    }

    relevant_keys = set(rename_dict.keys()).intersection(estate_dict.keys())
    result_dict = {}
    for k in relevant_keys:
        item_value = estate_dict[k]
        item_key = rename_dict[k]
        result_dict[item_key] = item_value
    return result_dict


def convert_types_in_estate_data(estate_dict) -> dict:
    cols_to_convert_to_int = [
        'estate_id',
        'price',
        'rooms',
        'living_area_size',
        'lot_size',
        'floor',
        'zipcode',
        'net',
        'exp',
        'construction_year',
        'basement_size',
        'sqm_price'
    ]
    data_cols = estate_dict.keys()
    relevant_cols = set(cols_to_convert_to_int).intersection(data_cols)
    for c in relevant_cols:
        estate_dict[c] = convert_str_to_int(estate_dict[c])
    return estate_dict


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
