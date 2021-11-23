from agent.utils import convert_str_to_int
import pytest


@pytest.mark.parametrize(
    'test_input, expected',
    [('5.1', 5), ('001.17', 1), ('-', None)]
)
def test_str_to_int(test_input, expected):
    assert convert_str_to_int(test_input) == expected
