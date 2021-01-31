import json
import re
from collections import namedtuple
from datetime import datetime

from connection_create import connect
from db_requests import GET_DATA, GET_POST, DELETE, UPDATE, INSERT_USER

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
    return json.loads('')


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
    cursor_data = cur.execute(GET_POST, {'unique_id': get_id(url)})
    if cursor_data is None:
        return ResponseStatus(404, 'application/json', {})
    post = load_data_to_json(cursor_data)
    cur.close()
    connection.close()
    return ResponseStatus(200, 'application/json', post)


def add_post(url=None, vars=None):
    connection = connect()
    cur = get_connection_cursor(connection)
    cursor_data = cur.execute(GET_POST, (vars['uniqueId'],))
    cur.close()
    if cursor_data is not None:
        return ResponseStatus(400, 'application/json', {})
    cur = get_connection_cursor(connection)
    user_id = cur.execute("SELECT userId FROM users WHERE username= %s", (vars['username'],))
    cur.close()
    if user_id is None:
        cur = get_connection_cursor(connection)
        user_id=cur.execute(INSERT_USER,
                    (vars['username'], vars['userKarma'], datetime.strptime(vars['userCakeDay'], '%Y-%m-%d')))
        connection.commit()
        cur.close()
        print(user_id)
        print(type(user_id))
    cur = get_connection_cursor(connection)
    cur.execute(INSERT_USER, (
        vars['uniqueId'], vars['postUrl'], vars["postKarma"], vars["commentKarma"],
        datetime.strptime(vars['postDate'], '%Y-%m-%d'),
        vars['numberOfComments'], vars['numberOfVotes'], vars['postCategory'], user_id))
    connection.commit()
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
                "usernames": vars['username'],
                "user_karma": vars['userKarma'],
                "user_CakeDay": vars['userCakeDay'],
                "post_karma": vars["postKarma"],
                "comment_karma": vars["commentKarma"],
                "post_date": vars["postDate"],
                "number_OfComments": vars['numberOfComments'],
                "number_OfVotes": vars['numberOfVotes'],
                "post_Category": vars['postCategory']
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
