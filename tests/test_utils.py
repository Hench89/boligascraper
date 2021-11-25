from agent.utils import convert_str_to_int, remove_numbers_and_special
import pytest


@pytest.mark.parametrize(
    'test_input, expected',
    [('5.1', 5), ('001.17', 1), ('-', None)]
)
def test_str_to_int(test_input, expected):
    assert convert_str_to_int(test_input) == expected


@pytest.mark.parametrize(
    'test_input, expected',
    [('#C', 'C'), ('##129939293z222', 'z')]
)
def test_that_str_can_be_stripped_from_special_chars(test_input, expected):
    assert remove_numbers_and_special(test_input) == expected
