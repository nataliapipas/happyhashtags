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
        self.logger.info("Initializing with {} {} {} {} {}".format(user, password, database, host, port))

    def writeToPostgres(self, rows: list, query: str):
        try:
            connection = psycopg2.connect(user=self.user,
                                          password=self.password,
                                          host=self.host,
                                          port=self.port,
                                          database=self.database)

            cursor = connection.cursor()

            cursor.executemany(read_query(query, self.logger), rows)
            connection.commit()
            self.logger.info("Executed query")

        except Exception as error:
            self.logger.info("Error while connecting to PostgreSQL", error)
        finally:
            # closing database connection.
            if connection:
                self.logger.info("Closing PostgreSQL")
                cursor.close()
                connection.close()
