import numpy as np
import re

def compare_number_sets(list_a, list_b):

    if list_a is None or list_b is None:
        return list_a or [], list_b or []

    # as lists
    list_a = np.int64(list_a)
    list_b = np.int64(list_b)

    # as sets
    seta = set(list_a)
    setb = set(list_b)

    # compare
    a_set_only = seta.difference(setb)
    set_intersection = setb.intersection(seta)
    b_set_only = setb.difference(seta)

    return a_set_only, set_intersection, b_set_only

def strip_digits(txt):
    trim = re.compile(r'[^\d]+')
    return trim.sub('', txt)
