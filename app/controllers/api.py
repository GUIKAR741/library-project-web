"""."""
from flask_restful import Resource, reqparse
from ..models.usuario import Usuario

parser = reqparse.RequestParser()


class UserCadastro(Resource):
    """."""

    def post(self):
        """."""
        from pymysql.err import IntegrityError
        parser.add_argument('nome', help='blank', required=True)
        parser.add_argument('email', help='blank', required=True)
        parser.add_argument('telefone', help='blank', required=False)
        parser.add_argument('cpf', help='blank', required=True)
        parser.add_argument('senha', help='blank', required=True)
        data = parser.parse_args()
        print(data)
        u = Usuario(data)
        u.criptografar_senha('senha')
        try:
            u.insert()
            return {
                'message': 'Usuario Cadastrado'
            }
        except IntegrityError as e:
            if 'email' in str(e):
                mensagem = 'Email já Cadastrado!'
            elif 'cpf' in str(e):
                mensagem = 'CPF já Cadastrado!'
            else:
                mensagem = 'Erro ao Cadastrar!'
            return {
                'message': mensagem
            }, 500
