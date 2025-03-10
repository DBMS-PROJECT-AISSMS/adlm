import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def execute_query(query, params=(), fetch_one=False, fetch_all=False):
    connection = pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            if fetch_one:
                return cursor.fetchone()
            if fetch_all:
                return cursor.fetchall()
            connection.commit()
