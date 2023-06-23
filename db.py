import psycopg2
from fastapi import HTTPException


class Database:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.conn = None

    def connect(self):
        try:
            if self.conn is None or self.conn.closed != 0:
                self.conn = psycopg2.connect(
                    host=self.host,
                    port=self.port,
                    database=self.database,
                    user=self.user,
                    password=self.password,
                )
                self.conn.autocommit = True
                print("PostgresSQL connected")
        except Exception as exc:
            print(exc)
            raise HTTPException(
                status_code=500,
                detail="An error occurred while processing the request.",
            )

    def disconnect(self):
        if self.conn is not None and self.conn.closed == 0:
            self.conn.close()

    def execute_query(self, query, *args):
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(query, args)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as exc:
            print(exc)
            raise HTTPException(
                status_code=500,
                detail="An error occurred while processing the request.",
            )

    def execute_query_one(self, query, *args):
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(query, args)
            result = cursor.fetchone()
            cursor.close()
            return result
        except Exception as exc:
            print(exc)
            raise HTTPException(
                status_code=500,
                detail="An error occurred while processing the request.",
            )

    def execute_query_insert(self, query, *args):
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(query, args)
            self.conn.commit()
            cursor.close()
        except Exception as exc:
            print(exc)
            raise HTTPException(
                status_code=500,
                detail="An error occurred while processing the request.",
            )
