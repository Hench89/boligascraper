from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import pandas as pd


def get_dk_lat_lng(address):
    try:
        geolocator = Nominatim(user_agent="myapp")
        loc = geolocator.geocode(query=address, language='da', country_codes='Denmark')
        lat_lon = loc.raw['lat'] + ',' + loc.raw['lon']
        return lat_lon
    except Exception:
        return ''

class StationDist:

    def __init__(self, stations_path: str):
        self.df_lat_lng = pd.read_csv(stations_path)

    def get_dist_to_station(self, zipcode, latlng):
        try:
            if zipcode == '' or latlng == '':
                return None
            point_a = self.df_lat_lng[str(zipcode)]
            point_b = latlng
            dist = geodesic(point_a, point_b).km
            return round(dist, 2)
        except Exception:
            return None
