import json
import re
from collections import namedtuple
from datetime import datetime
from db_requests import GET_DATA,GET_POST,DELETE,UPDATE
from connection_create import connect

ResponseStatus = namedtuple("ResponseStatus",
                            ["response", "ContentType", "data"])


def get_connection_cursor(connection):
    return connection.cursor()


def get_time():
    return datetime.today().strftime("%Y%m%d")


FILE_NAME = f'reddit-{get_time()}.txt'


def get_id(url):
    return re.match(r'/posts/(.+)/', url).group(1)  # id


def load_data_to_json(cursor_data):
    if cursor_data is None:
        return {}
    # как-то преобразовать
    return json.loads(f.read())


def get_file_data(url=None, vars=None):
    connection = connect()
    cur = get_connection_cursor(connection)
    cursor_data = cur.execute(GET_DATA)
    print(cursor_data)
    data = load_data_to_json(cursor_data)
    cur.close()
    connection.close()
    return ResponseStatus(200, 'application/json', data)


def get_post(url=None, vars=None):
    connection = connect()
    cur = get_connection_cursor(connection)
    cursor_data = cur.execute(GET_POST, {'uniqueId': get_id(url)})
    if cursor_data is None:
        return ResponseStatus(404, 'application/json', {})
    post = load_data_to_json(cursor_data)
    cur.close()
    connection.close()
    return ResponseStatus(200, 'application/json', post)


def add_post(url=None, vars=None):
    connection = connect()
    cur = get_connection_cursor(connection)
    cursor_data = cur.execute(GET_POST, {'uniqueId': get_id(url)})
    cur.close()
    if cursor_data is not None:
        return ResponseStatus(400, 'application/json', {})
    cur = get_connection_cursor()
    cur.execute("INSERT vars")
    cur.commit()
    cur.close()
    connection.close()
    return ResponseStatus(201, 'application/json', {"uniqueId": vars['uniqueId']})


def update_post(url=None, vars=None):
    connection = connect()
    cur = get_connection_cursor(connection)
    cursor_data = cur.execute(GET_POST, {'uniqueId': get_id(url)})
    cur.close()
    if cursor_data is not None:
        cur = get_connection_cursor()
        cur.execute(
            UPDATE,
            {
                "unique_id": get_id(url),
                "post_url": vars['postUrl'],
                "username": vars['username'],
                "userKarma": vars['userKarma'],
                "userCakeDay": vars['userCakeDay'],
                "postKarma": vars["postKarma"],
                "commentKarma": vars["commentKarma"],
                "postDate": vars["postDate"],
                "numberOfComments": vars['numberOfComments'],
                "numberOfVotes": vars['numberOfVotes'],
                "postCategory": vars['postCategory']
            })
        cur.commit()
        cur.close()
        return ResponseStatus(200, 'application/json', {})
    return ResponseStatus(404, 'application/json', {})


def remove_post(url=None, vars=None):
    connection = connect()
    cur = get_connection_cursor(connection)
    cursor_data = cur.execute(GET_POST, {'uniqueId': get_id(url)})
    cur.close()
    if cursor_data is not None:
        cur = get_connection_cursor()
        cur.execute(DELETE, {'uniqueId': get_id(url)})
        cur.commit()
        cur.close()
        return ResponseStatus(204, 'application/json', {})
    return ResponseStatus(404, 'application/json', {})
