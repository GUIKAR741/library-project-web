"""Controler das paginas iniciais."""
from flask import Blueprint, render_template
index = Blueprint("index", __name__)


@index.route("/")
def index_route():
    """Rota da pagina indice."""
    # return render_template('dashboard-modern.html')
    # res = current_app.db().select("select * from tb_usuario")
    return 'olá'


@index.route("/pag/<nome>")
@index.route("/pag/", defaults={'nome': 'index.html'})
def pagina(nome):
    """Rota da pagina indice."""
    return render_template('theme/'+nome)


@index.route("/documentation/<nome>")
@index.route("/documentation/", defaults={'nome': 'index.html'})
def doc(nome):
    """Rota da pagina indice."""
    return render_template('documentation/'+nome)
