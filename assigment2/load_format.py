import json

import requests


def load_to_txt(posts):
    return json.dumps(posts, ident=None)


def load_to_server(post):
    try:
        response = requests.post(f'http://localhost:8087:/posts/', post)
    except:
        response.text
