"""Modulo Principal do Projeto."""
from flask import Flask
from flask_restful import Api
from .models import configure as config_db


def start_app() -> Flask:
    """Inicia o App."""
    app = Flask(__name__)

    app.config.from_object("app.config.development")

    api_ext = Api(app)

    config_db(app)

    from .controllers import index
    app.register_blueprint(index)

    from .controllers import api

    api_ext.add_resource(api.UserCadastro, '/api/UserCadastro',
                         endpoint='api.userCadastro')

    return app
