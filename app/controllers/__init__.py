"""Controler das paginas iniciais."""
from flask import Blueprint

index = Blueprint("index", __name__)


@index.route("/")
def index_route():
    """Rota da pagina indice."""
    return 'olá'
