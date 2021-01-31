import psycopg2

from config import config


def create_table(connection):
    cur = connection.cursor()
    cur.execute(
        "CREATE TABLE posts ("
        "uniqueId SERIAL PRIMARY KEY,"
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
        "userCakeDay INTEGER);"
    )
    connection.commit()
    cur.close()


def connect():
    try:
        connection_params = config()
        #create_table(connection)
        return psycopg2.connect(**connection_params)
    except Exception:
        print("Connection error")
