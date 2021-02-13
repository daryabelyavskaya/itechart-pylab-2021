from datetime import datetime

from adapters.database.db_base import AbstractDB
from pymongo import MongoClient


def get_time():
    return datetime.today().strftime("%Y-%m-%d")


def get_date(query):
    d = {}
    if query.get("postDate_min"):
        d['postDate'] = {"$gte": query['postDate_min']}
        if query.get("postDate_max"):
            d['postDate']['$lte'] = query['postDate_max']
        return d
    if query.get("postDate_max"):
        d['postDate'] = {'postDate': {"$lte": query['postDate_max']}}
        return d
    return {}


def get_comments(query):
    d = {}
    if query.get("numberOfComments_min"):
        d['numberOfComments'] = {"$gte": query['numberOfComments_min']}
        if query.get("numberOfComments_max"):
            d['numberOfComments']['$lte'] = query['numberOfComments_max']
        return d
    if query.get("numberOfComments_max"):
        d['numberOfComments'] = {'numberOfComments': {"$lte": query['numberOfComments_max']}}
        return d
    return {}


def get_query_attrs(query):
    if query.get("postCategory"):
        return {**get_date(query), **get_comments(query), "postCategory": query["postCategory"]}
    return {**get_date(query), **get_comments(query)}


class MongoDB(AbstractDB):

    def __init__(self, config):
        self.config = config
        client = self.connect()
        self.db = client[self.config.database_name]

    def connect(self):
        return MongoClient(self.config.host, self.config.port)

    def get_post_info(self, args):
        post = self.db.posts.find({'uniqueId': args})
        if post is None:
            return post
        return list(dict(post))

    def get_posts_data(self, query=None):
        query_attr = get_query_attrs(query)
        if query.get('limit'):
            return list(self.db.posts.find(query_attr, {'_id': 0})
                        .limit(int(query['limit']))
                        .skip(int(query['offset'])))
        return list(self.db.posts.find(query_attr, {'_id': 0}))

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
