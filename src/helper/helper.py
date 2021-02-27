from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from datetime import datetime, date
import locale

try:
    import locale
    locale.setlocale(locale.LC_ALL, 'da_DK.utf8')
except Exception:
    locale.setlocale(locale.LC_ALL, 'da_DK.UTF-8')

#locale.setlocale(locale.LC_TIME, "da_DK")
geolocator = Nominatim(user_agent="myapp")
stationLatLng = {
    '3450': '55.8722219179645,12.357256289318334',
    '3500': '55.78267401357219,12.373435113274889',
    '3460': '55.84059183837736,12.423737141941611',
    '2830': '55.796150423758895,12.471720175688658',
    '2800': '55.7683378432892, 12.502917749001524',
}


def get_lat_lng(address):
    try:
        loc = geolocator.geocode(query=address, language='da', country_codes='Denmark')
        return loc.raw['lat'] + ',' + loc.raw['lon']

    except AttributeError:
        return ''


def get_dist_to_station(zipcode, latlng):
    try:
        
        if zipcode == '' or latlng == '':
            return

        point_a = stationLatLng[str(zipcode)]
        point_b = latlng
        dist = geodesic(point_a, point_b).km
    
    except KeyError:
        return

    return round(dist, 2)


def days_on_market(date_string):
    try:
        today_date = date.today()
        date_string = str(date_string)[:10]
        created_date = datetime.strptime(date_string, '%Y-%m-%d').date()
        return (today_date - created_date).days
    except ValueError:
        return ''
