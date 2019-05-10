"""Modulo Principal do Projeto."""
from flask import Flask
from flaskext.mysql import MySQL


mysql = MySQL()


def start_app():
    """Inicia o App."""
    app = Flask(__name__)

    app.config.from_object("app.config.development")

    mysql.init_app(app)
    from .controllers import index
    app.register_blueprint(index)

    return app
