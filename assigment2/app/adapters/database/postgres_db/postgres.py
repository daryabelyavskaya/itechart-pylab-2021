from datetime import datetime

import psycopg2
from adapters.database.db_base import AbstractDB

from .db_requests import (
    GET_DATA,
    GET_POST,
    INSERT_USER,
    INSERT_POST,
    GET_USER_ID,
    UPDATE_USER,
    UPDATE_POST,
    DELETE_POST,
    DELETE_USER
)


def postgres_add_filter(query, request):
    s = ''
    f = False
    if query.get('postCategory'):
        f = True
        s += f"postCategory='{query['postCategory']}' AND "
    if query.get('numberOfComments_min'):
        f = True
        s += f"numberOfComments>='{query['numberOfComments_min']}' AND "
    if query.get('numberOfComments_max'):
        f = True
        s += f"numberOfComments<='{query['numberOfComments_max']}' AND "
    if query.get('postDate_min'):
        f = True
        s += f"postDate >='{query['postDate_min']}' AND "
    if query.get('postDate_max'):
        f = True
        s += f"postDate <='{query['postDate_max']}' AND "
    if f:
        s = "WHERE " + s[:-4] + ';'
    if query.get('limit'):
        s = s[:-1] + f"LIMIT {query['limit']} OFFSET {query['offset']}"
    return request[:-1] + s


def get_time():
    return datetime.today().strftime("%Y-%m-%d")


class PostgresqlDB(AbstractDB):

    def __init__(self, config):
        self.config = config

    def connect(self):
        return psycopg2.connect(host=self.config.host,
                                database=self.config.database_name,
                                user=self.config.user,
                                password=self.config.password)

    @staticmethod
    def load_data_to_json(cursor_data):
        if cursor_data == [None]:
            return [{}]
        data = []
        for _ in cursor_data:
            data.append({
                "uniqueId": _[0],
                "postUrl": _[1],
                "username": _[11],
                "userKarma": _[12],
                "userCakeDay": _[13],
                "postKarma": _[3],
                "commentKarma": _[4],
                "postDate": _[5].strftime('%Y-%m-%d'),
                "numberOfComments": _[6],
                "numberOfVotes": _[7],
                "postCategory": _[8]
            })
        return data

    def get_post_info(self, args):
        connection = self.connect()
        connection_cursor = self.get_connection_cursor(connection)
        connection_cursor.execute(GET_POST, (args,))
        cursor_data = connection_cursor.fetchone()
        data = self.load_data_to_json([cursor_data])
        connection_cursor.close()
        connection.close()
        return data

    def get_posts_data(self, query=None):
        db_request = postgres_add_filter(query, GET_DATA)
        connection = self.connect()
        connection_cursor = self.get_connection_cursor(connection)
        connection_cursor.execute(db_request)
        cursor_data = connection_cursor.fetchall()
        data = self.load_data_to_json(cursor_data)
        connection_cursor.close()
        connection.close()
        return data

    @staticmethod
    def get_connection_cursor(connection):
        return connection.cursor()

    def check_user(self, connection, username):
        connection_cursor = self.get_connection_cursor(connection)
        connection_cursor.execute(GET_USER_ID, (username,))
        check = connection_cursor.fetchone()
        connection_cursor.close()
        return check

    def get_user_id(self, connection, args):
        connection_cursor = self.get_connection_cursor(connection)
        connection_cursor.execute(GET_USER_ID, (args,))
        user_id = connection_cursor.fetchone()
        connection_cursor.close()
        if user_id is not None:
            return user_id[0]
        return user_id

    def insert_user(self, connection, args):
        connection_cursor = self.get_connection_cursor(connection)
        connection_cursor.execute(
            INSERT_USER,
            (
                args['username'],
                args['userKarma'],
                datetime.strptime(args['userCakeDay'], '%Y-%m-%d')
            )
        )
        connection.commit()
        connection_cursor.close()

    def insert_post(self, args, ):
        connection = self.connect()
        check = self.check_user(connection, args['username'])
        if check is None:
            self.insert_user(connection, args)
        user_id = self.get_user_id(connection, args['username'])
        connection_cursor = self.get_connection_cursor(connection)
        connection_cursor.execute(
            INSERT_POST,
            (
                args['uniqueId'],
                args['postUrl'],
                args["postKarma"],
                args["commentKarma"],
                datetime.strptime(args['postDate'], '%Y-%m-%d'),
                args['numberOfComments'],
                args['numberOfVotes'],
                args['postCategory'],
                user_id,
                get_time()
            )
        )
        connection.commit()
        connection_cursor.close()
        connection.close()

    def delete_post(self, args):
        connection = self.connect()
        self.delete_user(
            connection,
            self.get_user_id(connection, args)
        )
        connection_cursor = self.get_connection_cursor(connection)
        connection_cursor.execute(DELETE_POST, (args,))
        connection.commit()
        connection_cursor.close()
        connection.close()

    def delete_user(self, connection, args):
        connection_cursor = self.get_connection_cursor(connection)
        connection_cursor.execute(DELETE_USER, (args,))
        connection.commit()
        connection_cursor.close()

    def update_posts(self, args, post_id):
        connection = self.connect()
        connection_cursor = self.get_connection_cursor(connection)
        connection_cursor.execute(
            UPDATE_POST, (
                post_id,
                args['postUrl'],
                args["postKarma"],
                args["commentKarma"],
                args["postDate"],
                args['numberOfComments'],
                args['numberOfVotes'],
                args['postCategory'],
                get_time(),
                post_id)
        )
        connection.commit()
        connection_cursor.close()
        connection.close()

    def update_user(self, connection, args, post_id):
        connection_cursor = self.get_connection_cursor(connection)
        connection_cursor.execute(
            UPDATE_USER,
            (args['username'],
             args['userKarma'],
             args['userCakeDay'],
             post_id)
        )
        connection.commit()
        connection_cursor.close()
