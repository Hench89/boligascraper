import numpy as np
import re

def compare_number_sets(list_a, list_b):

    if list_a is None or list_b is None:
        return list_a or [], list_b or []

    # cast as sets
    seta = set(np.int64(list_a))
    setb = set(np.int64(list_b))

    # find differences
    a_set_only = seta.difference(setb)
    set_intersection = setb.intersection(seta)
    b_set_only = setb.difference(seta)

    return list(a_set_only), list(set_intersection), list(b_set_only)

def strip_digits(txt):
    try:
        trim = re.compile(r'[^\d]+')
        stripped = trim.sub('', txt)
        return int(stripped)
    except Exception:
        return None

