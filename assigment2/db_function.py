from datetime import datetime

from db_requests import GET_POST, INSERT_USER, INSERT_POST, GET_DATA, GET_USER_ID, UPDATE_USER, UPDATE_POST, \
    DELETE_POST, DELETE_USER


def get_time():
    return datetime.today().strftime("%Y-%m-%d")


def get_cursor_post(connection, args):
    cur = get_connection_cursor(connection)
    cur.execute(GET_POST, (args,))
    cursor_data = cur.fetchone()
    cur.close()
    return cursor_data


def get_connection_cursor(connection):
    return connection.cursor()


def check_user(connection, username):
    cur = get_connection_cursor(connection)
    cur.execute(GET_USER_ID, (username,))
    check = cur.fetchone()
    cur.close()
    return check


def get_user_id(connection, args):
    cur = get_connection_cursor(connection)
    cur.execute(GET_USER_ID, (args,))
    user_id = cur.fetchone()
    cur.close()
    if user_id is not None:
        return user_id[0]
    return user_id


def insert_user(connection, args):
    cur = get_connection_cursor(connection)
    cur.execute(INSERT_USER,
                (args['username'], args['userKarma'], datetime.strptime(args['userCakeDay'], '%Y-%m-%d')))
    connection.commit()
    cur.close()


def insert_post(connection, args, user_id):
    cur = get_connection_cursor(connection)
    cur.execute(INSERT_POST, (
        args['uniqueId'], args['postUrl'], args["postKarma"], args["commentKarma"],
        datetime.strptime(args['postDate'], '%Y-%m-%d'),
        args['numberOfComments'], args['numberOfVotes'], args['postCategory'], user_id, get_time()))
    connection.commit()
    cur.close()


def get_db_data(connection):
    cur = get_connection_cursor(connection)
    cur.execute(GET_DATA)
    cursor_data = cur.fetchall()
    cur.close()
    return cursor_data


def delete_post(connection, args):
    cur = get_connection_cursor(connection)
    cur.execute(DELETE_POST, (args,))
    connection.commit()
    cur.close()


def delete_user(connection, args):
    cur = get_connection_cursor(connection)
    cur.execute(DELETE_USER, (args,))
    connection.commit()
    cur.close()


def update_posts(connection, args, post_id):
    cur = get_connection_cursor(connection)

    cur.execute(
        UPDATE_POST, (post_id, args['postUrl'], args["postKarma"],
                      args["commentKarma"], args["postDate"], args['numberOfComments'], args['numberOfVotes'],
                      args['postCategory'], get_time(), post_id))
    connection.commit()
    cur.close()


def update_user(connection, args, post_id):
    cur = get_connection_cursor(connection)
    cur.execute(
        UPDATE_USER, (args['username'], args['userKarma'], args['userCakeDay'], post_id))
    connection.commit()
    cur.close()
