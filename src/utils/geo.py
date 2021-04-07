from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.exc import GeocoderServiceError
from utils.numbers import strip_postal_code

def get_dk_geo(address):

    # fetch postalcode
    postal_code = strip_postal_code(address)
    parts = address.split(',')

    # deconstruct parts
    street_parts = [p.strip() for p in parts if postal_code not in p]
    zip_parts = [p.strip() for p in parts if postal_code in p]
    city_parts = [z.replace(postal_code, '').strip() for z in zip_parts]

    # setup query dict
    qdict = {'country' : 'DK'}
    if len(postal_code)>0:
        qdict['postalcode'] = postal_code
    if len(city_parts)>0:
        qdict['city'] = city_parts[0]
    if len(street_parts)>0:
        qdict['street'] = ', '.join(street_parts)

    # try with all
    geolocator = Nominatim(user_agent="myapp")
    loc = geolocator.geocode(query=qdict)
    if loc is not None:
        return loc.raw['lat'] + ',' + loc.raw['lon']

    # try without city
    geolocator = Nominatim(user_agent="myapp")
    loc = geolocator.geocode(query=qdict.pop('city'))
    if loc is not None:
        return loc.raw['lat'] + ',' + loc.raw['lon']

    print('.. could not find latlng for address: %s' % address)
    return None


def km_dist(point_a, point_b):
    return round(geodesic(point_a, point_b).km, 2)


def get_geo_details(address, stations):

    d = {}
    d['latlon'] = ''
    d['gmaps'] = ''
    d['station_dist_km'] = ''
    
    # get latlon from address
    d['latlon'] = get_dk_geo(address)
        
        # calculate distance to nearest s-train station
        stations_latlng = [str(s['lat']) + ',' + str(s['lon']) for s in stations]
        distances = [km_dist(s, d['latlon']) for s in stations_latlng]
        distances = [d for d in distances if d is not '']
        d['station_dist_km'] = str(min(distances))
    
    return d
