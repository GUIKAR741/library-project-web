"""Controller das rotas da biblioteca."""
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    jsonify
    )
from flask_login import login_required, current_user
from ..models.livro import Livro
from ..models.exemplar import Exemplar
from ..models.emprestimo import Emprestimo
from ..models.reserva import Reserva
from ..models.forms import UserForm
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
    reservas = Livro().select(
        "select count(id) as total from reserva "
        "where usuario_id=%(uid)s and status=1",
        {'uid': current_user.id},
        ).total
    reservas = Livro().select(
        "select count(id) as total from reserva "
        "where usuario_id=%(uid)s and status=1",
        {'uid': current_user.id},
        ).total
    emprestimos = Livro().select(
        "select count(id) as total from emprestimo "
        "where usuario_id=%(uid)s and status=0",
        {'uid': current_user.id},
        ).total
    devolucao = Livro().select(
        "select data_devolucao_estimada from emprestimo "
        "where usuario_id=%(uid)s and status=0 "
        "ORDER BY data_devolucao_estimada",
        {'uid': current_user.id},
    ).data_devolucao_estimada
    return render_template('home.html',
                           livros=livro,
                           qtdlivro=total,
                           reservas=reservas,
                           emprestimos=emprestimos,
                           devolucao=devolucao)


@library.route('/library/acervo/', defaults={'id': 1})
@library.route('/library/acervo/<int:id>')
@login_required
def acervo(id):
    """."""
    livro = Livro()
    if 'livro' in request.args.keys():
        livros = livro.select(
            "SELECT id, titulo, autor, capa, ano, editora "
            "FROM livro WHERE titulo LIKE %(livro)s",
            {'livro': '%' + request.args['livro'] + '%'},
            sel='fetchall'
        )
        lista = [[]]
        for i in livros:
            if len(lista[-1]) < 4:
                lista[-1].append(i)
            else:
                lista.append([])
                lista[-1].append(i)
        total = len(lista)
    else:
        itemsPagina = 12
        inicio = (id - 1) * itemsPagina
        total = livro.select("SELECT count(id) as total FROM livro").total
        livros = livro.select(
            "SELECT id, titulo, autor, capa, ano, editora "
            "FROM livro LIMIT %(inicio)s, %(items)s",
            {'inicio': inicio, "items": itemsPagina},
            sel='fetchall'
            )
        total = ceil(total/itemsPagina)
        lista = [[]]
        for i in livros:
            if len(lista[-1]) < 4:
                lista[-1].append(i)
            else:
                lista.append([])
                lista[-1].append(i)
    return render_template('acervo.html', lista=lista, total=total, pagina=id)


@library.route('/library/perfil/', methods=['GET', 'POST'])
@login_required
def perfil():
    """."""
    formulario = UserForm()
    if request.method == 'GET':
        formulario.nome.data = current_user.nome
        formulario.cpf.data = current_user.cpf
        formulario.email.data = current_user.email
        formulario.telefone.data = current_user.telefone
        return render_template('perfil.html', form=formulario), 200
    else:
        if formulario.validate_on_submit():
            if current_user.verify_password('senha', formulario.senha.data):
                try:
                    current_user.nome = formulario.nome.data
                    current_user.email = formulario.email.data
                    current_user.telefone = formulario.telefone.data
                    if formulario.novaSenha.data == formulario\
                            .confNovaSenha.data:
                        if (not (formulario.novaSenha.data == '')):
                            current_user.senha = formulario.novaSenha.data
                            current_user.criptografar_senha('senha')
                    else:
                        return jsonify({
                            'msg': 'Senhas Diferentes!'
                            })
                    current_user.update('id', current_user.id)
                    return jsonify({
                        'status': 'ok',
                        'msg': 'Atualizado Com Sucesso!'
                        })
                except Exception:
                    return jsonify({'msg': 'Erro ao Atualizao'})
            else:
                return jsonify({'msg': 'Senha Errada!'})
        else:
            return jsonify({'msg': 'Erro!'})


@library.route('/library/reservas/', defaults={'id': 0})
@library.route('/library/reservas/<int:id>')
@login_required
def reservas(id):
    """."""
    r = Reserva()
    if id != 0:
        r.status = 0
        r.update('id', val=id)
    livros = r.select(
        """
        select r.id, r.livro_id, l.titulo from reserva r
        join livro l on l.id=r.livro_id
        where usuario_id=%(id)s and status=1""",
        {'id': current_user.id},
        'fetchall'
        )
    res = []
    for i in livros:
        ll = r.select(
            "SELECT l.titulo, ee.data_devolucao_estimada "
            "FROM livro as l JOIN exemplar as e "
            "ON l.id=e.livro_id "
            "JOIN emprestimo as ee "
            "ON ee.exemplar_id=e.id "
            "WHERE l.id=%(id)s AND ee.status=0 "
            "ORDER BY ee.data_devolucao_estimada LIMIT 1",
            {'id': i.livro_id}
            )
        res.append(
            {
                'idReserva': i.id,
                'titulo': i.titulo,
                'data_devolucao_estimada':
                    ll.data_devolucao_estimada if ll else None
            }
        )
    return render_template('minhas-reservas.html', reservas=res)


@library.route('/library/emprestimos/',
               defaults={'renovacao': 'false', 'id': 0})
@library.route('/library/emprestimos/<string:renovacao>/<int:id>')
@login_required
def emprestimos(renovacao, id):
    """."""
    emprestimo = Emprestimo()
    erro = 'False'
    if renovacao == 'renovacao' and (id != 0 and id > 0):
        emp = emprestimo.select(
            "select ex.livro_id from emprestimo e "
            "JOIN exemplar ex ON e.exemplar_id=ex.id "
            "where e.id=%(id)s and e.usuario_id=%(uid)s",
            {'id': id, 'uid': current_user.id}
        )
        qtd_res = emprestimo.select("SELECT COUNT(r.livro_id) as qtd_reserva "
                                    "FROM emprestimo as ee "
                                    "JOIN exemplar as e "
                                    "ON ee.exemplar_id=e.id "
                                    "JOIN livro as l "
                                    "ON e.livro_id= l.id "
                                    "JOIN reserva as r "
                                    "ON l.id=r.livro_id "
                                    "WHERE l.id=%(id)s and r.status=1",
                                    {'id': emp.livro_id})
        if qtd_res.qtd_reserva == 0:
            emp = emp.select("SELECT id, renovacao FROM emprestimo "
                             "where id=%(id)s and usuario_id=%(uid)s",
                             {"id": id, 'uid': current_user.id})
            emp._op(
                '''
                UPDATE emprestimo SET renovacao = renovacao+1,
                data_devolucao_estimada =
                DATE_ADD(data_devolucao_estimada, INTERVAL 1 MONTH)
                WHERE id = %(idE)s
                ''',
                {'idE': emp.id}
            )
            erro = {'msg': "Renovado Com Sucesso!", 'icon': 'success'}
        else:
            erro = {
                'msg':
                "Não Foi Possivel Renovar Livro já Reservado!",
                'icon': 'error'
                }
    elif renovacao == 'comprovante' and (id != 0 and id > 0):
        emprest = Emprestimo()
        e = emprest.select("SELECT ee.id, l.titulo, e.codigo, "
                           "ee.data_emprestimo, d.data_devolucao, d.multa, "
                           "ee.status "
                           "FROM emprestimo ee JOIN exemplar e "
                           "ON ee.exemplar_id=e.id "
                           "LEFT JOIN devolucao d on ee.id=d.emprestimo_id "
                           "JOIN livro l ON e.livro_id=l.id "
                           "WHERE ee.usuario_id=%(id)s and ee.id=%(ide)s",
                           {'id': current_user.id, 'ide': id})
        return render_template('comprovante.html', dados=e, user=current_user)
    emps = emprestimo.select(
        "SELECT ee.id, l.titulo, ee.data_devolucao_estimada, "
        "ee.renovacao, ee.status, d.data_devolucao, d.multa "
        "FROM emprestimo ee JOIN exemplar e ON ee.exemplar_id=e.id "
        "LEFT JOIN devolucao d ON ee.id=d.emprestimo_id "
        "JOIN livro l ON e.livro_id=l.id "
        "WHERE ee.usuario_id=%(id)s",
        {'id': current_user.id},
        'fetchall'
        )
    return render_template('meus-emprestimos.html',
                           emprestimos=emps,
                           erro=erro)


@library.route('/library/informacoes/', defaults={'id': -1, 'res': 'vazio'})
@library.route('/library/informacoes/<id>', defaults={'res': 'vazio'})
@library.route('/library/informacoes/<id>/<string:res>')
@login_required
def informacoes(id, res):
    """."""
    if int(id) <= 0:
        return redirect(url_for('library.home'))
    exemplares = Exemplar().select(
        'SELECT id, disponivel from exemplar '
        'where livro_id=%(livro_id)s',
        {'livro_id': id}, sel='fetchall'
        )
    disp = len(list(filter(lambda x: x.disponivel == 1,
                           exemplares)))
    erro = 'False'
    if res == 'reservar':
        re = Reserva()
        if len(re.select("SELECT id FROM reserva "
                         "WHERE livro_id=%(lid)s and usuario_id=%(uid)s and "
                         "status=1", {'lid': id, 'uid': current_user.id},
                         'fetchall')) == 0 and disp == 0:
            re.livro_id = id
            re.usuario_id = current_user.id
            re.insert()
            erro = {
                'titulo': "Reserva Realizada com Sucesso!",
                "msg": '',
                'icon': 'success'
                }
        else:
            erro = {
                'titulo': "Erro ao Fazer Reserva!",
                "msg": 'Possiveis Motivos: '
                       'Livro Possui Exemplares Disponiveis, '
                       'Você já Fez uma Reserva desse Livro.',
                'icon': 'error'
                }
    livro = Livro().select(
        "select titulo, autor, capa, ano, editora, descricao "
        "from livro where id = %(id)s",
        {'id': id}
        )
    return render_template('informacoes.html',
                           livro=livro,
                           total=len(exemplares),
                           disponiveis=disp,
                           erro=erro)
