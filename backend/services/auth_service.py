from backend.db import fetch_one


def authenticate_user(username_or_email, password):
    query = """
        SELECT user_id, username, role, first_name, last_name
        FROM users
        WHERE (username = %s OR email = %s) AND password = %s
    """
    return fetch_one(query, (username_or_email, username_or_email, password))
