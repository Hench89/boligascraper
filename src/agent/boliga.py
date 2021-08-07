import requests
import math
import pandas as pd

class BoligaEstate:

    def __init__(self):
        self.estate_endpoint = 'https://api.boliga.dk/api/v2/estate/'


    def fetch_estate_data(self, estate_id: str):
        url = f'{self.estate_endpoint}{estate_id}'
        data = requests.get(url).json()
        df = pd.DataFrame([data])
        return df


class BoligaList:

    def __init__(self):
        self.forsale_api = 'https://api.boliga.dk/api/v2/search/results'
        self.sold_api = 'https://api.boliga.dk/api/v2/sold/search/results'


    def get_forsale_data(self, zipcodes: list):
        return self.fetch_api_to_df(zipcodes, self.forsale_api)


    def get_sold_data(self, zipcodes: list):
        return self.fetch_api_to_df(zipcodes, self.sold_api)


    def fetch_api_to_df(self, zipcodes: list, api_endpoint: str) -> pd.DataFrame:
        all_entries = []
        for z in zipcodes:
            all_entries += self.get_list_data_from_zipcode(api_endpoint, z)
        df = pd.DataFrame(all_entries)
        return df


    def make_url(self, api_endpoint:str, page = None, pagesize = None, zipcode = None):
        parameters = []
        parameters += [f'page={page}'] if page is not None else []
        parameters += [f'pagesize={pagesize}'] if pagesize is not None else []
        parameters += [f'zipcodeFrom={zipcode}'] if zipcode is not None else []
        parameters += [f'zipcodeTo={zipcode}'] if zipcode is not None else []
        joined_params = '&'.join(parameters)
        return f'{api_endpoint}?{joined_params}'


    def get_list_data_from_zipcode(self, api_endpoint: str, zipcode: str):
        n = self.get_api_pages_for_zipcode(api_endpoint, zipcode)
        json_entries = []
        for p in range(1, n+1):
            url = self.make_url(api_endpoint, page=p, pagesize=500, zipcode=zipcode)
            data = requests.get(url).json()
            results = data['results']
            print(f'Fetching list data from "{api_endpoint}" endpoint - {zipcode} with (page {p} of {n})')
            json_entries += [i for i in results]
        return json_entries


    def get_api_pages_for_zipcode(self, api_endpoint: str, zipcode: str):
        url = self.make_url(api_endpoint, page=1, zipcode=zipcode)
        data = requests.get(url).json()
        total_count = data['meta']['totalCount']
        api_calls_required = math.ceil(total_count / 500)
        return api_calls_required
