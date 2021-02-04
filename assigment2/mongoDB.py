from datetime import datetime

from pymongo import MongoClient


def get_time():
    return datetime.today().strftime("%Y-%m-%d")


class MongoDB:
    def __init__(self, config):
        self.config = config

    def connection(self):
        client = MongoClient()
        self.db = client.posts
        self.db.createCollection("posts", {'capped': True, max: 1000})

    def get_cursor_post(self, args):
        return self.db.posts.find({'uniqueId': args})

    def get_db_data(self):
        return self.db.users.find()

    def insert_post(self, args):
        self.db.posts.insert({
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
        self.db.remove({'uniqueId': args})

    def update_posts(self, connection, args, post_id):
        self.db.posts({'uniqueId': post_id}, {
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
