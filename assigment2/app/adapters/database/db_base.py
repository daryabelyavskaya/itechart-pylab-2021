from abc import abstractmethod, ABC


class AbstractDB(ABC):

    @abstractmethod
    def connect(self):
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
        pass

    @abstractmethod
    def update_posts(self, connection, args, post_id):
        pass
