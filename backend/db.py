import psycopg2
import psycopg2.extras

from backend.config import Config


def get_db_connection():
    return psycopg2.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        dbname=Config.DB_NAME,
    )


def fetch_one(query, params=()):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cursor.execute(query, params)
        return cursor.fetchone()
    finally:
        cursor.close()
        connection.close()


def fetch_all(query, params=()):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cursor.execute(query, params)
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def execute(query, params=()):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def execute_returning_one(query, params=()):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cursor.execute(query, params)
        result = cursor.fetchone()
        connection.commit()
        return result
    finally:
        cursor.close()
        connection.close()
