import pandas as pd
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from datetime import datetime, date
import locale

locale.setlocale(locale.LC_TIME, "da_DK")
geolocator = Nominatim(user_agent="myapp")
stationLatLng = {
    '3450': '55.8722219179645,12.357256289318334',
    '3500': '55.78267401357219,12.373435113274889',
    '3460': '55.84059183837736,12.423737141941611',
    '2830': '55.796150423758895,12.471720175688658',
    '2800': '55.7683378432892, 12.502917749001524',
}


def get_lat_lng(address):
    #try:
    loc = geolocator.geocode(query=address, language='da', country_codes='Denmark')
    return loc.raw['lat'] + ',' + loc.raw['lon']

    #except:
    #    return ''


def get_dist_to_station(zipcode, latlng):

    if zipcode == '' or latlng == '':
        return

    point_a = stationLatLng[str(zipcode)]
    point_b = latlng
    dist = geodesic(point_a, point_b).km
    return round(dist, 2)


def days_on_market(date_string):
    try:
        today_date = date.today()
        date_string = str(date_string)[:10]
        created_date = datetime.strptime(date_string, '%Y-%m-%d').date()
        return (today_date - created_date).days
    except ValueError:
        return ''


def write_to_excel(df, path):

    # setup writer
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)

    # Get the xlsxwriter workbook and worksheet objects.
    worksheet = writer.sheets['Sheet1']

    # Format: cell width
    for c in df.columns:
        i = df.columns.get_loc(c)
        values_len = df[c].astype(str).str.len().max()
        header_len = len(c)
        worksheet.set_column(i, i + 1, max(values_len, header_len))

    # Format: auto filter
    max_row = df.shape[0]
    max_col = df.shape[1]
    worksheet.autofilter(0, 0, max_row, max_col - 1)

    # set CreatedDate as hidden
    worksheet.set_column('O:O', None, None, {'hidden': True})

    writer.save()
