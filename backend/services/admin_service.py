from backend.db import execute, fetch_all


def get_users(exclude_user_id=None):
    if exclude_user_id is None:
        return fetch_all(
            "SELECT user_id, first_name, last_name, email, role FROM users ORDER BY user_id"
        )

    query = """
        SELECT user_id, first_name, last_name, email, role
        FROM users
        WHERE user_id != %s
        ORDER BY user_id
    """
    return fetch_all(query, (exclude_user_id,))


def add_user(username, password, email, role, first_name, last_name):
    query = """
        INSERT INTO users (username, password, email, role, first_name, last_name)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    execute(query, (username, password, email, role, first_name, last_name))


def delete_user(user_id):
    execute("DELETE FROM users WHERE user_id = %s", (user_id,))
