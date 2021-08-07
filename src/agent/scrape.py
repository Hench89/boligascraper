import pandas as pd
from boliga import BoligaList, BoligaEstate
from archive import RawArchive
import sys


def set_comparison(list_a: list, list_b: list):
    seta = set(map(int, set(list_a)))
    setb = set(map(int, set(list_b)))
    left = seta.difference(setb)
    inner = setb.intersection(seta)
    right = setb.difference(seta)
    return left, inner, right


def fetch_forsale_list(zipcodes: list):
    forsale_data = boliga_list.get_forsale_data(zipcodes)
    archive.save_forsale_list(forsale_data)


def fetch_forsale_estate():
    forsale_list_ids = archive.get_forsale_list_ids()
    forsale_archive_ids = archive.get_forsale_archive_ids()
    new_ids, ids_in_common, remove_ids = set_comparison(forsale_list_ids, forsale_archive_ids)
    print(f'new: {len(new_ids)}, removed: {len(remove_ids)}, no change: {len(ids_in_common)}')

    for index, estate_id in enumerate(new_ids):
        print(f'fetching estate {estate_id} - ({index+1} of {len(new_ids)})')
        estate_data = boliga_estate.fetch_estate_data(estate_id)
        archive.save_forsale_estate(estate_data, estate_id)


def fetch_sold_list(zipcodes: list):
    sold_data = boliga_list.get_sold_data(zipcodes)
    archive.save_sold_list(sold_data)


def fetch_sold_estate():
    sold_list_ids = archive.get_sold_list_ids()
    sold_archive_ids = archive.get_sold_archive_ids()
    new_ids, ids_in_common, remove_ids = set_comparison(sold_list_ids, sold_archive_ids)
    print(f'new: {len(new_ids)}, removed: {len(remove_ids)}, no change: {len(ids_in_common)}')

    ids_to_fetch = [x for x in new_ids if x != 0]

    for index, estate_id in enumerate(ids_to_fetch):
        print(f'fetching estate {estate_id} - ({index+1} of {len(ids_to_fetch)})')
        estate_data = boliga_estate.fetch_estate_data(estate_id)
        archive.save_sold_estate(estate_data, estate_id)


if __name__ == "__main__":

    zipcodes_path = './static/zipcodes.csv'
    zipcodes = pd.read_csv(zipcodes_path)['zipcode'].tolist()

    boliga_list = BoligaList()
    boliga_estate = BoligaEstate()
    archive = RawArchive()

    if archive.get_list_freshness() < 0:
        print('latest data is pretty new - no need to refresh anything!')
        sys.exit(0)

    fetch_forsale_list(zipcodes)
    fetch_forsale_estate()
    fetch_sold_list(zipcodes)
    fetch_sold_estate()
