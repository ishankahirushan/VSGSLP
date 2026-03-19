from backend.db import fetch_all


def get_workshops():
    query = """
        SELECT w.workshop_id, w.workshop_name, w.workshop_description, w.start_time, z.zoom_link
        FROM workshops w
        LEFT JOIN workshop_zoom_links z ON w.workshop_id = z.workshop_id
        ORDER BY w.start_time NULLS LAST, w.workshop_name
    """
    return fetch_all(query)


def get_social_media_groups():
    query = """
        SELECT group_id, course_name, platform, group_link, created_by
        FROM social_media_groups
        ORDER BY platform, course_name
    """
    return fetch_all(query)


def get_announcements():
    query = "SELECT id, title, summary, date FROM announcements ORDER BY date DESC"
    return fetch_all(query)
