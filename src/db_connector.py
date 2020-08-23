import psycopg2
from os_utils import read_query


class DbConnector:
    def __init__(self, user, password, database, host, logger, port='5432'):
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.port = port
        self.logger = logger

    def writeRows(self, rows: list, query: str):
        """
        Writes rows to the database using a query
        :param rows:
        :param query:
        :return:
        """
        connection = self.connect()
        try:
            with connection.cursor() as cursor:
                cursor.executemany(read_query(query, self.logger), rows)
                connection.commit()
        except Exception as e:
            connection.rollback()
            raise e

    def connect(self):
        """
        Opens a connection to the database
        :return: The connection
        """
        return psycopg2.connect(user=self.user,
                                password=self.password,
                                host=self.host,
                                port=self.port,
                                database=self.database)
