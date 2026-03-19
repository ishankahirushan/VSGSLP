from flask import Flask
from pathlib import Path

from backend.config import Config
from backend.routes.api_routes import register_api_routes
from backend.routes.web_routes import register_web_routes


def create_app():
    project_root = Path(__file__).resolve().parent.parent
    app = Flask(
        __name__,
        template_folder=str(project_root / "templates"),
        static_folder=str(project_root / "static"),
    )
    app.config.from_object(Config)

    register_web_routes(app)
    register_api_routes(app)

    return app
