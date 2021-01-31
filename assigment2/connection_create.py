import psycopg2

from config import config


def create_table(connection):
    cur = connection.cursor()
    cur.execute(
        "CREATE TABLE posts ("
        "uniqueId VARCHAR PRIMARY KEY,"
        "postUrl VARCHAR,"
        "userId SMALLINT,"
        "postKarma INTEGER,"
        "commentKarma INTEGER,"
        "postDate DATE ,"
        "numberOfComments INTEGER,"
        "numberOfvotes INTEGER,"
        "postCategory VARCHAR);"
    )
    cur.execute(
        "CREATE TABLE users ("
        "userId SERIAL PRIMARY KEY,"
        "username VARCHAR,"
        "userKarma INTEGER,"
        "userCakeDay DATE);"
    )
    connection.commit()
    cur.close()


def connect():
    connection_params = config()
    # connection = psycopg2.connect(**connection_params)
    # create_table(connection)
    # cur = connection.cursor()
    # connection.commit()
    # cur.close()
    # connection.close()
    return psycopg2.connect(**connection_params)


# connect()
