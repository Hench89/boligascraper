from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from datetime import datetime, date
import pandas as pd
import re

class BoligaHelper:

    def __init__(self, stations_path: str):
        self.geolocator = Nominatim(user_agent="myapp")
        self._clean_cols = ['boliga_id', 'address1', 'address2', 'zipcode', 'list_price', 'living_area',
                'lot_area', 'rooms', 'floors', 'construction_date', 'energy_rating',
                'taxes_pr_month', 'bsmnt_area', 'station_dist_km', 'created_date', 'url', 'gmaps']
        self.df_lat_lng = pd.read_csv(stations_path)


    def get_lat_lng(self, address):
        try:
            loc = self.geolocator.geocode(query=address, language='da', country_codes='Denmark')
            return loc.raw['lat'] + ',' + loc.raw['lon']

        except AttributeError:
            return ''
        except:
            return ''


    def get_dist_to_station(self, zipcode, latlng):

        try:

            if zipcode == '' or latlng == '':
                return

            point_a = self.df_lat_lng[str(zipcode)]
            point_b = latlng
            dist = geodesic(point_a, point_b).km

        except KeyError:
            return

        return round(dist, 2)


    def days_on_market(self, date_string):
        try:
            today_date = date.today()
            date_string = str(date_string)[:10]
            created_date = datetime.strptime(date_string, '%Y-%m-%d').date()
            return (today_date - created_date).days
        except ValueError:
            return ''


    def _date_clean(self, x):
        x = x.replace('Oprettet ', '').replace('.', '')
        date_value = datetime.strptime(x, '%d %b %Y')
        return date_value


    def make_fancy(self, df):

        # rename some columns
        df = df.rename(
            columns={
                '#icon-square': 'living_area',
                '#icon-lot-size': 'lot_area',
                '#icon-rooms': 'rooms',
                '#icon-floor': 'floors',
                '#icon-construction-year': 'construction_date',
                '#icon-energy': 'energy_rating',
                '#icon-taxes': 'taxes_pr_month',
                '#icon-basement-size': 'bsmnt_area',

            }
        )

        # split address
        df['address1'] = df['address'].apply(lambda x: x.split(',')[0])
        df['address2'] = df['address'].apply(lambda x: x.split(',')[1])
        df = df.drop(columns=['address'])

        # numerical columns
        trim = re.compile(r'[^\d]+')
        df['list_price'] = df['list_price'].apply(lambda x: trim.sub('', x))
        df['living_area'] = df['living_area'].apply(lambda x: trim.sub('', x))
        df['lot_area'] = df['lot_area'].apply(lambda x: trim.sub('', x))
        df['floors'] = df['floors'].apply(lambda x: trim.sub('', x))
        df['taxes_pr_month'] = df['taxes_pr_month'].apply(lambda x: trim.sub('', x))
        df['bsmnt_area'] = df['bsmnt_area'].apply(lambda x: trim.sub('', x))

        # created date
        df['created_date'] = df['created_date'].apply(lambda x: self._date_clean(x))

        # geo related data
        df['latlng'] = df['address1'].apply(lambda x: self.get_lat_lng(x))
        df['gmaps'] = df['latlng'].apply(lambda x: 'https://maps.google.com/?q=' + str(x))
        df['station_dist_km'] = df.apply(lambda x: self.get_dist_to_station(x.zipcode, x.latlng), axis=1)

        return df[self._clean_cols]


    def get_empty_archive(self) -> pd.DataFrame:
        return pd.DataFrame(self._clean_cols)
