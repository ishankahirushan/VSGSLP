import psycopg2
from flask import jsonify, request, session

from backend.routes.helpers import admin_required_api, login_required_api
from backend.services.admin_service import add_user, delete_user, get_users
from backend.services.announcement_service import edit_announcement, list_announcements, post_announcement
from backend.services.auth_service import authenticate_user
from backend.services.dashboard_service import get_social_media_groups, get_workshops
from backend.services.group_service import (
    add_social_group,
    create_group,
    get_available_groups,
    get_group_by_id,
    get_group_members,
    get_joined_groups,
    join_group,
)


def register_api_routes(app):
    @app.route("/api/auth/login", methods=["POST"])
    def api_login():
        payload = request.get_json(silent=True) or {}
        username = (payload.get("username") or "").strip()
        password = payload.get("password") or ""

        if not username or not password:
            return jsonify({"error": "username and password are required"}), 400

        try:
            user = authenticate_user(username, password)
        except psycopg2.Error as err:
            print(f"API login error: {err}")
            return jsonify({"error": "database error"}), 500

        if not user:
            return jsonify({"error": "invalid credentials"}), 401

        session["user_id"] = user["user_id"]
        session["username"] = user["username"]
        session["role"] = user["role"]
        session["full_name"] = f"{user['first_name']} {user['last_name']}"

        return jsonify({"user": user})

    @app.route("/api/auth/logout", methods=["POST"])
    def api_logout():
        session.clear()
        return jsonify({"message": "logged out"})

    @app.route("/api/auth/me", methods=["GET"])
    @login_required_api
    def api_me():
        return jsonify(
            {
                "user_id": session.get("user_id"),
                "username": session.get("username"),
                "role": session.get("role"),
                "full_name": session.get("full_name"),
            }
        )

    @app.route("/api/dashboard", methods=["GET"])
    @login_required_api
    def api_dashboard():
        user_id = session["user_id"]
        try:
            return jsonify(
                {
                    "workshops": get_workshops(),
                    "social_groups": get_social_media_groups(),
                    "available_groups": get_available_groups(user_id),
                    "joined_groups": get_joined_groups(user_id),
                    "users": get_users(exclude_user_id=user_id),
                    "announcements": list_announcements(),
                }
            )
        except psycopg2.Error as err:
            print(f"API dashboard error: {err}")
            return jsonify({"error": "database error"}), 500

    @app.route("/api/groups", methods=["POST"])
    @login_required_api
    def api_create_group():
        payload = request.get_json(silent=True) or {}
        group_name = (payload.get("group_name") or "").strip()
        description = (payload.get("description") or "").strip()

        if not group_name or not description:
            return jsonify({"error": "group_name and description are required"}), 400

        try:
            group = create_group(group_name, description, session["user_id"])
            return jsonify({"group": group}), 201
        except psycopg2.Error as err:
            print(f"API create group error: {err}")
            return jsonify({"error": "database error"}), 500

    @app.route("/api/groups/available", methods=["GET"])
    @login_required_api
    def api_available_groups():
        try:
            return jsonify({"groups": get_available_groups(session["user_id"])})
        except psycopg2.Error as err:
            print(f"API available groups error: {err}")
            return jsonify({"error": "database error"}), 500

    @app.route("/api/groups/joined", methods=["GET"])
    @login_required_api
    def api_joined_groups():
        try:
            return jsonify({"groups": get_joined_groups(session["user_id"])})
        except psycopg2.Error as err:
            print(f"API joined groups error: {err}")
            return jsonify({"error": "database error"}), 500

    @app.route("/api/groups/<int:group_id>", methods=["GET"])
    @login_required_api
    def api_group_detail(group_id):
        try:
            group = get_group_by_id(group_id)
            if not group:
                return jsonify({"error": "group not found"}), 404
            members = get_group_members(group_id)
            return jsonify({"group": group, "members": members})
        except psycopg2.Error as err:
            print(f"API group detail error: {err}")
            return jsonify({"error": "database error"}), 500

    @app.route("/api/groups/<int:group_id>/join", methods=["POST"])
    @login_required_api
    def api_join_group(group_id):
        try:
            join_group(group_id, session["user_id"])
            return jsonify({"message": "joined"})
        except psycopg2.Error as err:
            print(f"API join group error: {err}")
            return jsonify({"error": "database error"}), 500

    @app.route("/api/social-groups", methods=["GET"])
    @login_required_api
    def api_social_groups():
        try:
            return jsonify({"groups": get_social_media_groups()})
        except psycopg2.Error as err:
            print(f"API social groups error: {err}")
            return jsonify({"error": "database error"}), 500

    @app.route("/api/social-groups", methods=["POST"])
    @login_required_api
    def api_add_social_group():
        payload = request.get_json(silent=True) or {}
        course_name = (payload.get("course_name") or "").strip()
        platform = (payload.get("platform") or "").strip()
        group_link = (payload.get("group_link") or "").strip()

        if not course_name or platform not in {"facebook", "linkedin"} or not group_link:
            return jsonify({"error": "invalid payload"}), 400

        try:
            add_social_group(course_name, platform, group_link, session["user_id"])
            return jsonify({"message": "created"}), 201
        except psycopg2.Error as err:
            print(f"API add social group error: {err}")
            return jsonify({"error": "database error"}), 500

    @app.route("/api/admin/users", methods=["GET"])
    @admin_required_api
    def api_get_users():
        try:
            return jsonify({"users": get_users(exclude_user_id=session["user_id"])})
        except psycopg2.Error as err:
            print(f"API users error: {err}")
            return jsonify({"error": "database error"}), 500

    @app.route("/api/admin/users", methods=["POST"])
    @admin_required_api
    def api_add_user():
        payload = request.get_json(silent=True) or {}
        required_fields = ["username", "password", "email", "role", "first_name", "last_name"]
        if not all(payload.get(field) for field in required_fields):
            return jsonify({"error": "missing required fields"}), 400

        try:
            add_user(
                payload["username"],
                payload["password"],
                payload["email"],
                payload["role"],
                payload["first_name"],
                payload["last_name"],
            )
            return jsonify({"message": "created"}), 201
        except psycopg2.Error as err:
            print(f"API add user error: {err}")
            return jsonify({"error": "database error"}), 500

    @app.route("/api/admin/users/<int:user_id>", methods=["DELETE"])
    @admin_required_api
    def api_delete_user(user_id):
        try:
            delete_user(user_id)
            return jsonify({"message": "deleted"})
        except psycopg2.Error as err:
            print(f"API delete user error: {err}")
            return jsonify({"error": "database error"}), 500

    @app.route("/api/announcements", methods=["GET"])
    @login_required_api
    def api_announcements():
        try:
            return jsonify({"announcements": list_announcements()})
        except psycopg2.Error as err:
            print(f"API announcements error: {err}")
            return jsonify({"error": "database error"}), 500

    @app.route("/api/announcements", methods=["POST"])
    @admin_required_api
    def api_post_announcement():
        payload = request.get_json(silent=True) or {}
        title = (payload.get("title") or "").strip()
        summary = (payload.get("summary") or "").strip()

        if not title or not summary:
            return jsonify({"error": "title and summary are required"}), 400

        try:
            post_announcement(title, summary)
            return jsonify({"message": "created"}), 201
        except psycopg2.Error as err:
            print(f"API post announcement error: {err}")
            return jsonify({"error": "database error"}), 500

    @app.route("/api/announcements/<int:announcement_id>", methods=["PUT"])
    @admin_required_api
    def api_edit_announcement(announcement_id):
        payload = request.get_json(silent=True) or {}
        title = (payload.get("title") or "").strip()
        summary = (payload.get("summary") or "").strip()

        if not title or not summary:
            return jsonify({"error": "title and summary are required"}), 400

        try:
            edit_announcement(announcement_id, title, summary)
            return jsonify({"message": "updated"})
        except psycopg2.Error as err:
            print(f"API edit announcement error: {err}")
            return jsonify({"error": "database error"}), 500
