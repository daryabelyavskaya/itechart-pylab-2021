import json
import re
from collections import namedtuple

from connection_create import connect
from db_function import get_cursor_post, get_user_id, insert_user, insert_post, get_db_data, \
    delete_post, update_posts, check_user, update_user, delete_user

ResponseStatus = namedtuple("ResponseStatus",
                            ["response", "ContentType", "data"])


def get_id(url):
    return re.match(r'/posts/(.+)/', url).group(1)


def load_data_to_json(cursor_data):
    print(cursor_data)
    if cursor_data is None:
        return {}
    return cursor_data


def get_data(url=None, args=None):
    connection = connect()
    cursor_data = get_db_data(connection)
    data = load_data_to_json(cursor_data)
    connection.close()
    return ResponseStatus(200, 'application/json', data)


def get_post(url=None, args=None):
    connection = connect()
    cursor_data = get_cursor_post(connection, get_id(url))
    if cursor_data is None:
        return ResponseStatus(404, 'application/json', {})
    post = load_data_to_json(cursor_data)
    connection.close()
    return ResponseStatus(200, 'application/json', post)


def add_post(url=None, args=None):
    connection = connect()
    cursor_data = get_cursor_post(connection, args['uniqueId'])
    if cursor_data is not None:
        return ResponseStatus(400, 'application/json', {})
    check = check_user(connection, args['username'])
    if check is None:
        insert_user(connection, args)
        user_id = get_user_id(connection, args['uniqueId'])
    insert_post(connection, args, user_id)
    connection.close()
    return ResponseStatus(201, 'application/json', {"uniqueId": args['uniqueId']})


def update_post(url=None, args=None):
    connection = connect()
    print('AAAAAAAAAAAAAAAAAa')
    cursor_data = get_cursor_post(connection, args['uniqueId'])
    if cursor_data is not None:
        update_posts(connection, args, get_id(url))
        update_user(connection, args, get_user_id(connection, get_id(url)))
        return ResponseStatus(200, 'application/json', {})
    return ResponseStatus(404, 'application/json', {})


def remove_post(url=None, args=None):
    connection = connect()
    cursor_data = get_cursor_post(connection, get_id(url))
    print(cursor_data)
    if cursor_data is None:
        delete_post(connection, get_id(url))
        delete_user(connection, get_user_id(connection, get_id(url)))
        return ResponseStatus(204, 'application/json', {})
    return ResponseStatus(404, 'application/json', {})
