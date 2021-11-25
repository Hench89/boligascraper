import os, re


def convert_str_to_int(txt: str):
    if not isinstance(txt, str):
        txt = str(txt)
    items = re.findall(r'\d+', txt)
    if len(items) == 0:
        return None
    result = int(items[0])
    return result


def remove_numbers_and_special(txt: str):
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
