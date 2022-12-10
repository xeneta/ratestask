from psycopg2 import connect


class DbHandle:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.db_connection = None
        self.cursor = None

    def connect_db(self):
        self.db_connection = connect(
        host=self.host,
        port=self.port,
        database=self.database,
        user=self.user,
        password=self.password
        )
        self.cursor = self.db_connection.cursor()

    def execute_query(self, query):
        self.cursor.execute(query)
        queried_data = self.cursor.fetchall()
        return queried_data

    def close_db_connection(self):
        self.db_connection.close()
