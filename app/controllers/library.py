"""Controller das rotas da biblioteca."""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..models.livro import Livro
from ..models.exemplar import Exemplar
from math import ceil

library = Blueprint('library', __name__)


@library.route('/library/')
@login_required
def home():
    """."""
    total = Livro().select(
        "select count(id) as total from livro"
        ).total
    livro = Livro().select(
        "select id, titulo, autor, capa, ano, editora from livro limit 4",
        sel='fetchall'
        )
    return render_template('home.html', livros=livro, qtdlivro=total)


@library.route('/library/acervo/', defaults={'id': 1})
@library.route('/library/acervo/<int:id>')
@login_required
def acervo(id):
    """."""
    itemsPagina = 12
    inicio = (id - 1) * itemsPagina
    livro = Livro()
    total = livro.select("SELECT count(id) as total FROM livro").total
    livros = livro.select(
        "SELECT id, titulo, autor, capa, ano, editora FROM livro LIMIT %(inicio)s, %(items)s",
        {'inicio': inicio, "items": itemsPagina},
        sel='fetchall'
        )
    lista = [[]]
    total = ceil(total/itemsPagina)
    print(total)
    for i in livros:
        if len(lista[-1]) < 4:
            lista[-1].append(i)
        else:
            lista.append([])
            lista[-1].append(i)
    return render_template('acervo.html', lista=lista, total=total, pagina=id)


@library.route('/library/perfil/')
@login_required
def perfil():
    """."""
    return render_template('perfil.html', user=current_user)


@library.route('/library/reservas/')
@login_required
def reservas():
    """."""
    return render_template('minhas-reservas.html')


@library.route('/library/emprestimos/')
@login_required
def emprestimos():
    """."""
    return render_template('meus-emprestimos.html')


@library.route('/library/informacoes/', defaults={'id': -1})
@library.route('/library/informacoes/<id>')
@login_required
def informacoes(id):
    """."""
    if int(id) <= 0:
        return redirect(url_for('library.home'))
    livro = Livro().select(
        "select titulo, autor, capa, ano, editora, descricao "
        "from livro where id = %(id)s",
        {'id': id}
        )
    exemplares = Exemplar().select(
        'SELECT id, disponivel from exemplar where livro_id=%(livro_id)s',
        {'livro_id': id}, sel='fetchall'
        )
    return render_template('informacoes.html',
                           livro=livro,
                           total=len(exemplares),
                           disponiveis=len(list(filter(lambda x: x.disponivel == 1,
                                                       exemplares))))
