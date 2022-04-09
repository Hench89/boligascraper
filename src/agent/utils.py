import re
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




