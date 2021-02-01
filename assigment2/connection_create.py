import psycopg2

from config import config


def trigger(connection):
    cur = connection.cursor()
    cur.execute("CREATE OR REPLACE FUNCTION check_number_of_row() RETURNS TRIGGER AS $body$\n"
                "BEGIN\n"
                "    IF (SELECT count(*) FROM posts) > 1000 THEN \n"
                "       RAISE EXCEPTION 'INSERT statement exceeding maximum number of rows for this table'; \n"
                "    END IF;\n"
                "END;\n"
                "$body$\n"
                "LANGUAGE plpgsql;\n"
                "CREATE TRIGGER tr_check_number_of_row \n"
                "BEFORE INSERT ON posts\n"
                "FOR EACH ROW EXECUTE PROCEDURE check_number_of_row();\n")
    cur.close()
    connection.commit()


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
        "postCategory VARCHAR,"
        "postAddedDate DATE);"
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


def drop_table(connection):
    cur = connection.cursor()
    cur.execute("DROP TABLE users, posts")
    connection.commit()
    cur.close()
    connection.close()


def connect():
    connection_params = config()
    connection = psycopg2.connect(**connection_params)
    #trigger(connection)
    # drop_table(connection)
    # create_table(connection)
    return connection


#connect()
