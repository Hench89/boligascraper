import re

def compare_number_sets(list_a, list_b):

    if list_a is None or list_b is None:
        return list_a or [], list_b or []

    # cast as sets
    seta = set(list_a)
    setb = set(list_b)

    # find differences
    a_set_only = seta.difference(setb)
    set_intersection = setb.intersection(seta)
    b_set_only = setb.difference(seta)

    return list(a_set_only), list(set_intersection), list(b_set_only)


def strip_digits(txt):
    try:
        p = re.compile(r'[^\d]+')
        stripped = p.sub('', txt)
        return int(stripped)
    except Exception:
        return None

def strip_postal_code(txt):
    try:
        p = re.compile(r'\d\d\d\d')
        result = [r.strip() for r in p.findall(txt)]
        return result[0]
    except Exception:
        return None
