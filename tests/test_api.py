import pytest
from agent.boliga import (
    get_forsale_results,
    get_sold_results,
    get_estate_data,
    get_url_with_params,
    convert_types_in_estate_data
)


def test_estate_data():
    data = get_estate_data(1829597)
    errors = []

    if not isinstance(data, dict):
        errors.append('expected data as dict')
    if not len(data.keys()) == 23:
        errors.append('didnt get expected number of keys in dict')
    if not isinstance(data['rooms'], int):
        errors.append('expected rooms as integer type')
    if not 'estate_id' in data.keys():
        errors.append('expected estate_id in all cols')

    assert not errors, "errors occured:\n{}".format("\n".join(errors))


def test_get_forsale_results():
    results = get_forsale_results(3450)
    errors = []

    if not len(results) > 10:
        errors.append('expected list size min not met')
    if not len(results) < 200:
        errors.append('expected list size max not met')
    if not 'estate_id' in results[0].keys():
        errors.append('expected estate_id in all cols')

    assert not errors, "errors occured:\n{}".format("\n".join(errors))


def test_get_sold_results():
    results = get_sold_results(3450)
    errors = []

    if not len(results) > 2000:
        errors.append('expected list size min not met')
    if not 'estate_id' in results[0].keys():
        errors.append('expected estate_id in all cols')

    assert not errors, "errors occured:\n{}".format("\n".join(errors))

@pytest.mark.parametrize(
    'endpoint, params, expected_url',
    [
        ('www.google.com', {'page': 1}, 'www.google.com?page=1'),
        ('www.google.com', {'page': 1, 'name': 'abc'}, 'www.google.com?page=1&name=abc'),
        ('mysite.com', {'hello': 1, 'world': '1abc'}, 'mysite.com?hello=1&world=1abc')
    ]
)
def test_url_params(endpoint, params, expected_url):
    assert get_url_with_params(endpoint, params) == expected_url


def test_convert_cols_to_int():
    data = {'living_area_size': '500.000', 'dummy_col': True}
    expected_result = {'living_area_size': 500, 'dummy_col': True}
    result = convert_types_in_estate_data(data)
    assert result == expected_result
