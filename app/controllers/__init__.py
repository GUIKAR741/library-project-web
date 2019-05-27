"""Controler das paginas iniciais."""
from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    redirect,
    url_for
    )
from flask_login import login_user, current_user, login_required, logout_user
from ..models.forms import LoginForm
from ..models.usuario import Usuario

index = Blueprint("index", __name__)


@index.route("/", methods=['GET', 'POST'])
def login():
    """Rota da pagina login."""
    if not current_user.is_anonymous:
        return redirect(url_for("library.home"))
    form = LoginForm()
    if request.method == 'GET':
        return render_template("login.html", form=form), 200
    else:
        if form.validate_on_submit():
            user = Usuario().procurarUsuarioPeloEmail(form.usuario.data)
            if user and \
               user.verify_password('senha', form.senha.data) and \
               user.tipo == 0:
                login_user(user)
                return jsonify({'logado': True, 'msg': ''})
            else:
                return jsonify({'logado': False,
                                'msg': 'Credenciais do Usuario Incorretas!'})
        else:
            redirect(url_for('index.login'))


@index.route("/forgot")
def senha():
    """Rota da pagina login."""
    if not current_user.is_anonymous:
        return redirect(url_for("library.home"))
    return render_template("esqueceu-senha.html")


@index.route('/logout')
@login_required
def logout():
    """."""
    logout_user()
    return redirect(url_for('index.login'))


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
