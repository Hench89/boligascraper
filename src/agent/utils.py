import os, re, math, urllib
import pandas as pd


def convert_str_series_to_int64(s: pd.Series):
    s.apply(lambda x: convert_str_to_int(x))
    s_int64 = s.astype('Int64')
    return s_int64


def make_str_series_alphabetical(s: pd.Series):
    return s.apply(lambda x: make_str_alphabetical(x))


def convert_str_to_int(txt: str):
    if not isinstance(txt, str):
        txt = str(txt)
    items = re.findall(r'\d+', txt)
    if len(items) == 0:
        return None
    result = int(items[0])
    return result


def make_str_alphabetical(txt: str):
    if not isinstance(txt, str):
        txt = str(txt)
    items = re.findall('[a-zA-Z]+', txt)
    if len(items) == 0:
        return None
    return items[0]


def create_dirs_for_file(file_path: str):
    abs_file_path = os.path.abspath(file_path)
    dir_name = os.path.dirname(abs_file_path)
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)


def get_api_calls_required(total_count: int):
    return math.ceil(total_count / 500)


def get_url_with_params(endpoint: str, params: dict) -> str:
    params_encoded = urllib.parse.urlencode(params)
    return f'{endpoint}?{params_encoded}'


def a_diff_b(a, b) -> list:
    return set(a).difference(set(b))
