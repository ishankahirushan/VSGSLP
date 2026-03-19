import psycopg2
from flask import flash, jsonify, redirect, render_template, request, session, url_for

from backend.services.admin_service import add_user, delete_user, get_users
from backend.services.announcement_service import edit_announcement, post_announcement
from backend.services.auth_service import authenticate_user
from backend.services.dashboard_service import get_announcements, get_social_media_groups, get_workshops
from backend.services.group_service import (
    add_social_group,
    create_group,
    get_available_groups,
    get_group_by_id,
    get_group_members,
    get_joined_groups,
    join_group,
)
from backend.routes.helpers import admin_required_web, login_required_web


def register_web_routes(app):
    @app.route("/", methods=["GET", "POST"], endpoint="login")
    def login():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")

            try:
                user = authenticate_user(username, password)
            except psycopg2.Error as err:
                print(f"Error during login query: {err}")
                flash("An error occurred. Please try again.")
                user = None

            if user:
                session["user_id"] = user["user_id"]
                session["username"] = user["username"]
                session["role"] = user["role"]
                session["full_name"] = f"{user['first_name']} {user['last_name']}"
                return redirect(url_for("dashboard"))

            flash("Invalid username or password!")

        return render_template("login.html")

    @app.route("/logout", endpoint="logout")
    def logout():
        session.clear()
        flash("You have been logged out.")
        return redirect(url_for("login"))

    @app.route("/dashboard", endpoint="dashboard")
    @login_required_web
    def dashboard():
        user_id = session["user_id"]
        try:
            workshops = get_workshops()
            social_groups = get_social_media_groups()
            available_groups = get_available_groups(user_id)
            joined_groups = get_joined_groups(user_id)
            users = get_users(exclude_user_id=user_id)
            announcements = get_announcements()
        except psycopg2.Error as err:
            print(f"Error fetching dashboard data: {err}")
            flash("An error occurred while loading dashboard data.")
            workshops = []
            social_groups = []
            available_groups = []
            joined_groups = []
            users = []
            announcements = []

        return render_template(
            "db.html",
            full_name=session.get("full_name", "User"),
            role=session.get("role", "User"),
            workshops=workshops,
            social_groups=social_groups,
            available_groups=available_groups,
            joined_groups=joined_groups,
            users=users,
            announcements=announcements,
        )

    @app.route("/create_group", methods=["POST"], endpoint="create_group")
    @login_required_web
    def create_group_route():
        group_name = request.form.get("group_name", "").strip()
        description = request.form.get("description", "").strip()

        if not group_name or not description:
            flash("Group name and description are required.")
            return redirect(url_for("dashboard"))

        try:
            create_group(group_name, description, session["user_id"])
            flash("Study group created successfully!")
        except psycopg2.Error as err:
            print(f"Error creating group: {err}")
            flash("An error occurred while creating the group.")

        return redirect(url_for("dashboard"))

    @app.route("/join_group", methods=["POST"], endpoint="join_group")
    @login_required_web
    def join_group_route():
        group_id = request.form.get("group_id", "").strip()
        if not group_id.isdigit():
            flash("Invalid group id.")
            return redirect(url_for("dashboard"))

        try:
            join_group(int(group_id), session["user_id"])
            flash("Successfully joined the group!")
        except psycopg2.Error as err:
            print(f"Error joining group: {err}")
            flash("An error occurred while joining the group.")

        return redirect(url_for("dashboard"))

    @app.route("/view_group/<int:group_id>", endpoint="view_group")
    @login_required_web
    def view_group(group_id):
        try:
            group = get_group_by_id(group_id)
            if not group:
                flash("Group not found!")
                return redirect(url_for("dashboard"))

            members = get_group_members(group_id)
            return render_template("viewgroup.html", group=group, members=members)
        except psycopg2.Error as err:
            print(f"Error viewing group: {err}")
            flash("An error occurred while viewing the group.")
            return redirect(url_for("dashboard"))

    @app.route("/add_group", methods=["POST"], endpoint="add_group")
    @login_required_web
    def add_group_route():
        course_name = request.form.get("course_name", "").strip()
        platform = request.form.get("platform", "").strip()
        group_link = request.form.get("group_link", "").strip()

        if not course_name or platform not in {"facebook", "linkedin"} or not group_link:
            flash("Valid course name, platform, and group link are required.")
            return redirect(url_for("dashboard"))

        try:
            add_social_group(course_name, platform, group_link, session["user_id"])
            flash("New group added successfully!")
        except psycopg2.Error as err:
            print(f"Error adding new group: {err}")
            flash("An error occurred. Please try again.")

        return redirect(url_for("dashboard"))

    @app.route("/add_user", methods=["POST"], endpoint="add_user")
    @admin_required_web
    def add_user_route():
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        email = request.form.get("email", "").strip()
        role = request.form.get("role", "").strip()
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()

        if not all([username, password, email, role, first_name, last_name]):
            flash("All user fields are required.")
            return redirect(url_for("dashboard"))

        try:
            add_user(username, password, email, role, first_name, last_name)
            flash("User added successfully!")
        except psycopg2.Error as err:
            print(f"Error adding user: {err}")
            flash("An error occurred while adding the user.")

        return redirect(url_for("dashboard"))

    @app.route("/delete_user/<int:user_id>", methods=["POST"], endpoint="delete_user")
    @admin_required_web
    def delete_user_route(user_id):
        try:
            delete_user(user_id)
            flash("User deleted successfully!")
        except psycopg2.Error as err:
            print(f"Error deleting user: {err}")
            flash("An error occurred while deleting the user.")

        return redirect(url_for("dashboard"))

    @app.route("/get_users", methods=["GET"], endpoint="get_users")
    @admin_required_web
    def get_users_route():
        try:
            users = get_users(exclude_user_id=session["user_id"])
            return jsonify(users)
        except psycopg2.Error as err:
            print(f"Error fetching users: {err}")
            flash("An error occurred while fetching users.")
            return redirect(url_for("dashboard"))

    @app.route("/post_announcement", methods=["POST"], endpoint="post_announcement")
    @admin_required_web
    def post_announcement_route():
        title = request.form.get("title", "").strip()
        summary = request.form.get("summary", "").strip()

        if not title or not summary:
            flash("Title and summary are required.")
            return redirect(url_for("dashboard"))

        try:
            post_announcement(title, summary)
            flash("Announcement posted successfully!")
        except psycopg2.Error as err:
            print(f"Error posting announcement: {err}")
            flash("An error occurred while posting the announcement.")

        return redirect(url_for("dashboard"))

    @app.route("/edit_announcement/<int:announcement_id>", methods=["POST"], endpoint="edit_announcement")
    @admin_required_web
    def edit_announcement_route(announcement_id):
        title = request.form.get("title", "").strip()
        summary = request.form.get("summary", "").strip()

        if not title or not summary:
            flash("Title and summary are required.")
            return redirect(url_for("dashboard"))

        try:
            edit_announcement(announcement_id, title, summary)
            flash("Announcement updated successfully!")
        except psycopg2.Error as err:
            print(f"Error updating announcement: {err}")
            flash("An error occurred while updating the announcement.")

        return redirect(url_for("dashboard"))
