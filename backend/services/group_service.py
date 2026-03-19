from backend.db import execute, execute_returning_one, fetch_all, fetch_one


def get_available_groups(user_id):
    query = """
        SELECT sg.group_id, sg.group_name, sg.description, sg.created_by, sg.created_at
        FROM study_groups sg
        WHERE sg.group_id NOT IN (
            SELECT group_id FROM study_group_members WHERE user_id = %s
        )
        ORDER BY sg.created_at DESC
    """
    return fetch_all(query, (user_id,))


def get_joined_groups(user_id):
    query = """
        SELECT sg.group_id, sg.group_name, sg.description, sg.created_by, sg.created_at
        FROM study_groups sg
        JOIN study_group_members sgm ON sg.group_id = sgm.group_id
        WHERE sgm.user_id = %s
        ORDER BY sg.created_at DESC
    """
    return fetch_all(query, (user_id,))


def create_group(group_name, description, created_by):
    create_query = """
        INSERT INTO study_groups (group_name, description, created_by)
        VALUES (%s, %s, %s)
        RETURNING group_id
    """
    group = execute_returning_one(create_query, (group_name, description, created_by))
    execute(
        "INSERT INTO study_group_members (group_id, user_id) VALUES (%s, %s)",
        (group["group_id"], created_by),
    )
    return group


def join_group(group_id, user_id):
    execute(
        """
        INSERT INTO study_group_members (group_id, user_id)
        VALUES (%s, %s)
        ON CONFLICT (group_id, user_id) DO NOTHING
        """,
        (group_id, user_id),
    )


def get_group_by_id(group_id):
    return fetch_one("SELECT * FROM study_groups WHERE group_id = %s", (group_id,))


def get_group_members(group_id):
    query = """
        SELECT u.user_id, u.first_name, u.last_name, u.username, sgm.joined_at
        FROM users u
        JOIN study_group_members sgm ON u.user_id = sgm.user_id
        WHERE sgm.group_id = %s
        ORDER BY sgm.joined_at ASC
    """
    return fetch_all(query, (group_id,))


def add_social_group(course_name, platform, group_link, created_by):
    query = """
        INSERT INTO social_media_groups (course_name, platform, group_link, created_by)
        VALUES (%s, %s, %s, %s)
    """
    execute(query, (course_name, platform, group_link, created_by))
