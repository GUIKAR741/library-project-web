"""Modulo Principal do Projeto."""
from flask import Flask, render_template
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from .models import configure as config_db


def start_app() -> Flask:
    """Inicia o App."""
    app = Flask(__name__)

    app.config.from_object("app.config.development")

    config_db(app)

    login = LoginManager()

    login.init_app(app)

    app.crsf = CSRFProtect(app)

    @app.errorhandler(404)
    def page_not_found(e):  # pylint: disable=unused-variable
        """Erro Pagina não Encontrada."""
        return render_template('erro-404.html'), 404

    @app.errorhandler(500)
    def server_error(e):  # pylint: disable=unused-variable
        """Erro interno no servidor."""
        return render_template('erro-500.html'), 500

    @app.errorhandler(401)
    def unauthorized(e):  # pylint: disable=unused-variable
        """Redireciona caso o usuario não seja autorizado."""
        return render_template('erro-401.html'), 401

    @login.user_loader
    def load_user(user_id):  # pylint: disable=unused-variable
        """Carrega o Usuario Logado."""
        from .models.usuario import Usuario
        return Usuario().select("select * from usuario where id = %(user_id)s",
                                {'user_id': user_id})

    app.jinja_env.filters['datetime'] = (  # pylint: disable=no-member
        lambda value, format: value.strftime(format)
        )
    app.jinja_env.tests['maiorZero'] = (  # pylint: disable=no-member
        lambda x: len(x) > 0
    )

    from .controllers import index
    app.register_blueprint(index)

    from .controllers.library import library
    app.register_blueprint(library)

    return app
