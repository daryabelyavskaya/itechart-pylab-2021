from decouple import config


class DBConfig():
    port = config("PORT")
    host = config("HOST")
    database = config('DATABASE')
    database_name = config('DATABASE_NAME')
    user = config('CLIENT')
    password = config('PASSWORD')

    def configs(self):
        config_dict = {
            'port': self.port,
            'host': self.host,
            'database': self.database,
            'database_name': self.database_name,
            'user': self.user,
            'password': self.password
        }
        return config_dict
