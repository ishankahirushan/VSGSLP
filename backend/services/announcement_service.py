from backend.db import execute, fetch_all


def list_announcements():
    return fetch_all("SELECT id, title, summary, date FROM announcements ORDER BY date DESC")


def post_announcement(title, summary):
    execute("INSERT INTO announcements (title, summary) VALUES (%s, %s)", (title, summary))


def edit_announcement(announcement_id, title, summary):
    execute(
        """
        UPDATE announcements
        SET title = %s, summary = %s, date = CURRENT_TIMESTAMP
        WHERE id = %s
        """,
        (title, summary, announcement_id),
    )
