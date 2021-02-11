from datetime import datetime

from adapters.database.db_base import AbstractDB
from pymongo import MongoClient


def get_time():
    return datetime.today().strftime("%Y-%m-%d")


class MongoDB(AbstractDB):

    def __init__(self, config):
        self.config = config
        client = self.connect()
        self.db = client[self.config.database_name]

    def connect(self):
        return MongoClient(self.config.host, self.config.port)

    def get_cursor_post(self, args):
        return self.db.posts.find_one({'uniqueId': args}, {'_id': 0})

    def get_db_data(self):
        print(list(self.db.posts.find({}, {'_id': 0})))
        return list(self.db.posts.find({}, {'_id': 0}))

    def insert_post(self, args):
        self.db.posts.insert_one({
            "uniqueId": args['uniqueId'],
            "postUrl": args['postUrl'],
            "username": args['username'],
            "userKarma": args['userKarma'],
            "userCakeDay": args['userCakeDay'],
            "postKarma": args['postKarma'],
            "commentKarma": args['commentKarma'],
            "postDate": args['postDate'],
            "numberOfComments": args['numberOfComments'],
            "numberOfVotes": args['numberOfVotes'],
            "postCategory": args['postCategory'],
            'postAddedDate': get_time()
        })

    def delete_post(self, args):
        self.db.posts.delete_one({'uniqueId': args})

    def update_posts(self, args, post_id):
        self.db.posts.update_many({'uniqueId': post_id}, {"$set": {
            "uniqueId": args['uniqueId'],
            "postUrl": args['postUrl'],
            "username": args['username'],
            "userKarma": args['userKarma'],
            "userCakeDay": args['userCakeDay'],
            "postKarma": args['postKarma'],
            "commentKarma": args['commentKarma'],
            "postDate": args['postDate'],
            "numberOfComments": args['numberOfComments'],
            "numberOfVotes": args['numberOfVotes'],
            "postCategory": args['postCategory'],
            'postAddedDate': get_time()
        }})
