class AbstractDB(object):
    @abstractmethod
     def __init__(self,config):
        pass

    @abstractmethod
    def connection(self):
        pass

    @abstractmethod
    def get_cursor_post(self, args):
        pass

    @abstractmethod
    def get_db_data(self):
        pass

    @abstractmethod
    def insert_post(self, args):
        pass

    @abstractmethod
    def delete_post(self, args):
        self.db.remove({'uniqueId': args})

    @abstractmethod
    def update_posts(self, connection, args, post_id):
        pass
