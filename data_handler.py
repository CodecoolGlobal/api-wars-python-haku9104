from typing import List, Dict
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import database_connection


@database_connection.connection_handler
def save_registered_user(cursor: RealDictCursor, user, password):
    dict1 = {
        'user': user,
        'password': password
    }
    query = """
        INSERT INTO users
        VALUES (%(user)s, %(password)s)"""
    cursor.execute(query, dict1)


@database_connection.connection_handler
def get_hashed_password(cursor: RealDictCursor, user):
    basedict = {
        'user': user
    }
    query = """
        SELECT users.password
        FROM users
        WHERE users.username = %(user)s
        """
    cursor.execute(query, basedict)
    return cursor.fetchone()


@database_connection.connection_handler
def check_if_taken(cursor: RealDictCursor, user):
    basedict = {
        'user': user
    }
    query = """
        SELECT COUNT(users.username) as "usernames"
        FROM users
        WHERE users.username = %(user)s
        GROUP BY users.username
        """
    cursor.execute(query, basedict)
    return cursor.fetchone()
