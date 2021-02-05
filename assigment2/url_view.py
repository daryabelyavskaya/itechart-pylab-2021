import re
from collections import namedtuple

ResponseStatus = namedtuple("ResponseStatus",
                            ["response", "ContentType", "data"])


class URLView:
    def __init__(self, database,config):
        self.database = database(config)

    @staticmethod
    def get_id(url):
        return re.match(r'/posts/(.+)/', url).group(1)

    def get_data(self, url=None, args=None):
        cursor_data = self.database.get_db_data()
        if cursor_data is None:
            return ResponseStatus(404, 'application/json', {})
        return ResponseStatus(200, 'application/json', cursor_data)

    def get_post(self, url=None, args=None):
        cursor_data = self.database.get_cursor_post(self.get_id(url))
        if cursor_data is None:
            return ResponseStatus(404, 'application/json', {})
        return ResponseStatus(200, 'application/json', {})

    def add_post(self, url=None, args=None):
        cursor_data = self.database.get_cursor_post(args['uniqueId'])
        if cursor_data is not None:
            return ResponseStatus(400, 'application/json', {})
        self.database.insert_post(args)
        return ResponseStatus(201, 'application/json', {"uniqueId": args['uniqueId']})

    def update_post(self, url=None, args=None):
        cursor_data = self.database.get_cursor_post(args['uniqueId'])
        if cursor_data is not None:
            self.database.update_posts(args, self.get_id(url))
            return ResponseStatus(200, 'application/json', {})
        return ResponseStatus(404, 'application/json', {})

    def remove_post(self, url=None, args=None):
        cursor_data = self.database.get_cursor_post(self.get_id(url))
        if cursor_data is not None:
            self.database.delete_post(self.get_id(url))
            return ResponseStatus(204, 'application/json', {})
        return ResponseStatus(404, 'application/json', {})
