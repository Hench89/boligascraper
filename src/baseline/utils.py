import pandas as pd

def get_property_types():
    data = [
        [1, 'Villa', 'V'],
        [2, 'Rækkehus', 'R'],
        [3, 'Ejerlejlighed', 'E'],
        [4, 'Fritidshus', 'F'],
        [5, 'Andelsbolig', 'A'],
        [6, 'Landejendom', 'L'],
        [7, 'Helårsgrund', 'G'],
        [8, 'Fritidsgrund', 'G'],
        [9, 'Villalejlighed', 'VI'],
        [10, 'Andet', 'A']
    ]
    cols = ['property_id', 'property_name', 'alias']
    return pd.DataFrame(data, columns = cols)

def set_url(estate_id):
    if estate_id == 0:
        return '-'
    return f'https://www.boliga.dk/bolig/{estate_id}' if estate_id != 0 else ''
