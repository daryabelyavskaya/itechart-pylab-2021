from datetime import datetime

from pymongo import MongoClient

from abstractDB import AbstractDB


def get_time():
    return datetime.today().strftime("%Y-%m-%d")


class MongoDB(AbstractDB):

    def __init__(self, config):
        self.config = config
        print(self.config.port)
        client = MongoClient(self.config.host, self.config.port)
        self.db = client[self.config.database_name]

    def get_cursor_post(self, args):
        return self.db.posts.find_one({'uniqueId': args})

    def get_db_data(self):
        return self.db.posts.find()

    def insert_post(self, args):
        self.db.posts.insert_one({
            "uniqueId": args['uniqueId'],
            "postUrl": args['url'],
            "username": args['username'],
            "userKarma": args['userKarma'],
            "userCakeDay": args['userCakeday'],
            "postKarma": args['postKarma'],
            "commentKarma": args['commentKarma'],
            "postDate": args['postDate'],
            "numberOfComments": args['numberOfComments'],
            "numberOfVotes": args['numberOfVotes'],
            "postCategory": args['postCategory'],
            'postAddedDate': get_time()
        })

    def delete_post(self, args):
        self.db.delete_one({'uniqueId': args})

    def update_posts(self, connection, args, post_id):
        self.db.posts.update_one({'uniqueId': post_id}, {
            "uniqueId": args['uniqueId'],
            "postUrl": args['url'],
            "username": args['username'],
            "userKarma": args['userKarma'],
            "userCakeDay": args['userCakeday'],
            "postKarma": args['postKarma'],
            "commentKarma": args['commentKarma'],
            "postDate": args['postDate'],
            "numberOfComments": args['numberOfComments'],
            "numberOfVotes": args['numberOfVotes'],
            "postCategory": args['postCategory'],
            'postAddedDate': get_time()
        })
