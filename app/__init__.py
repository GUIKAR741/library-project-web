"""Modulo Principal do Projeto."""
from flask import Flask
from .models import configure as config_db


def start_app():
    """Inicia o App."""
    app = Flask(__name__)

    app.config.from_object("app.config.development")

    config_db(app)

    from .controllers import index
    app.register_blueprint(index)

    return app
