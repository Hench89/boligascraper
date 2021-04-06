import requests as r
from bs4 import BeautifulSoup
import minify_html
import zlib
import json


def dict_to_json(dict, file_path):
    output = json.dumps(dict)
    with open(file_path, 'w') as f:
        f.write(output)


def read_json(file_path):
    with open(file_path) as f:
        return json.load(f)


def get_soup_from_url(url):
    html = r.get(url)
    return BeautifulSoup(html.text, 'html.parser')


def get_decompressed_soup_from_file(file_path):
    with open(file_path, "rb") as f:
        bytes = f.read()
    decompressed_html = zlib.decompress(bytes)
    decoded_html = decompressed_html.decode('utf-8')
    return BeautifulSoup(decoded_html, 'html.parser')


def get_compressed_html_from_url(url):
    soup = get_soup_from_url(url)
    html = soup.prettify()
    minified_html = minify_html.minify(html, minify_js=False, minify_css=False)
    encoded_html = bytes(minified_html, encoding='utf-8')
    compressed_html = zlib.compress(encoded_html)
    return compressed_html
