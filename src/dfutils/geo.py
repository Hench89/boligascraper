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

def get_nearest_station(df_stations, point):

    def km_dist(point_a_lat, point_a_lng, point_b):
        point_a = "{0},{1}".format(point_a_lat, point_a_lng)
        return geodesic(point_a, point_b).km
    
    if point == '':
        return None

    df_stations['dist'] = df_stations.apply(lambda x: km_dist(x.lat, x.lon, point), axis=1)
    nearest_station = df_stations.loc[df_stations['dist'].idxmin()]
    return round(nearest_station['dist'],2)
