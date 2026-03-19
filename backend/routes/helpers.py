from functools import wraps

from flask import flash, jsonify, redirect, session, url_for


def login_required_web(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("You need to log in first!")
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)

    return wrapper


def admin_required_web(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session or session.get("role") != "admin":
            flash("You need to be an admin to perform this action!")
            return redirect(url_for("dashboard"))
        return view_func(*args, **kwargs)

    return wrapper


def login_required_api(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Authentication required"}), 401
        return view_func(*args, **kwargs)

    return wrapper


def admin_required_api(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session or session.get("role") != "admin":
            return jsonify({"error": "Admin role required"}), 403
        return view_func(*args, **kwargs)

    return wrapper
