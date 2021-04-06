from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.exc import GeocoderServiceError

def get_dk_geo(address):

    def get(address):
        try:
            geolocator = Nominatim(user_agent="myapp")
            loc = geolocator.geocode(query=address, language='da', country_codes='Denmark')
            latlon = loc.raw['lat'] + ',' + loc.raw['lon']
            return latlon
        except (GeocoderServiceError, AttributeError):
            return ''
    
    address_splitted = address.split(',') if ',' in address else None

    latlon = get(address)
    if latlon == '' and type(address_splitted) == list and len(address_splitted)>2:
        alt_address = address_splitted[0] + ',' + address_splitted[-1]
        latlon = get(alt_address)
        
    return latlon


def km_dist(point_a, point_b):
    return round(geodesic(point_a, point_b).km, 2)


def get_geo_details(address, stations):

    d = {}
    d['latlon'] = ''
    d['gmaps'] = ''
    d['station_dist_km'] = ''
    
    # get latlon from address
    d['latlon'] = get_dk_geo(address)
    d['gmaps'] = 'https://maps.google.com/?q=' + d['latlon']
    
    # calculate distance to nearest s-train station
    if d['latlon'] != '':
        stations_latlng = [str(s['lat']) + ',' + str(s['lon']) for s in stations]
        distances = [km_dist(s, d['latlon']) for s in stations_latlng]
        distances = [d for d in distances if d is not '']
        d['station_dist_km'] = str(min(distances))
    
    return d
