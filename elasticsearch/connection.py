import sys

import psycopg2

import settings

class PostgresDBManager:
    def __init__(self,query,values,is_update):
        self.query=query
        self.is_update=is_update
        self.values=values
        self.connection=psycopg2.connect(
            user = settings.POSTGRES_DB_USER,
            password = settings.POSTGRES_DB_PASSWORD,
            host = settings.POSTGRES_DB_HOST,
            port = settings.POSTGRES_DB_PORT,
            database = settings.POSTGRES_DB_NAME)

        self.cursor=self.connection.cursor()
        #self.cursor.excute(query)

    def __enter__(self):
        self.cursor.execute(self.query,self.values)
        if self.is_update ==True:
            self.connection.commit()
        return self.cursor

    def __exit__(self,exc_type, exc_value, exc_traceback):
        self.connection.close()
        self.cursor.close()
