import json
import os
import re
from collections import namedtuple
from datetime import datetime

ResponseStatus = namedtuple("ResponseStatus",
                            ["response", "ContentType", "data"])


def get_time():
    return datetime.today().strftime("%Y%m%d")


FILE_NAME = f'reddit-{get_time()}.txt'


def get_id(url):
    return re.match(r'/posts/(.+)/', url).group(1)  # id


def load_data_file(f):
    return json.loads(f.read())


def check_not_empty_file():
    return os.path.getsize(FILE_NAME) > 0


def get_file_data(url=None, vars=None):
    if os.path.isfile(FILE_NAME) and check_not_empty_file():
        with open(FILE_NAME, 'r') as f:
            data = load_data_file(f)
            return ResponseStatus(200, 'application/json', data)
    return ResponseStatus(404, 'application/json', {})


def get_post(url=None, vars=None):
    if os.path.isfile(FILE_NAME) and check_not_empty_file():
        with open(FILE_NAME, 'r') as f:
            posts_data = load_data_file(f)
            for post in posts_data:
                if post['uniqueId'] == get_id(url):
                    return ResponseStatus(200, 'application/json', posts_data[post])
    return ResponseStatus(404, 'application/json', {})


def add_post(url=None, vars=None):
    with open(FILE_NAME, 'w+') as f:
        posts_data = []
        if check_not_empty_file():
            posts_data = load_data_file(f)
            for post in posts_data:
                if post['uniqueId'] == vars['uniqueId']:
                    return ResponseStatus(400, 'application/json', {})
        posts_data.append(vars)
        f.write(json.dumps(posts_data))
        return ResponseStatus(201, 'application/json', {"uniqueId": vars['uniqueId']})


def update_post(url=None, vars=None):
    if os.path.isfile(FILE_NAME):
        with open(FILE_NAME, 'w+') as f:
            if check_not_empty_file():
                posts_data = load_data_file(f)
                for post_index in range(len(posts_data)):
                    if posts_data[post_index]['uniqueId'] == get_id(url):
                        posts_data[post_index] = vars
                        f.write(json.dumps(posts_data))
                        return ResponseStatus(200, 'application/json', {})
    return ResponseStatus(404, 'application/json', {})


def remove_post(url=None, vars=None):
    if os.path.isfile(FILE_NAME):
        with open(FILE_NAME, 'r+') as f:
            if check_not_empty_file():
                posts_data = load_data_file(f)
            for post_index in range(len(posts_data)):
                if posts_data[post_index]['uniqueId'] == get_id(url):
                    del posts_data[post_index]
                    print(posts_data)
                    f.seek(0)
                    f.truncate(0)
                    f.write(json.dumps(posts_data))
                    return ResponseStatus(204, 'application/json', {})
    return ResponseStatus(404, 'application/json', {})