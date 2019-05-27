"""."""
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    # jwt_refresh_token_required,
    # get_jwt_identity,
    # get_raw_jwt
    )
from ..models.usuario import Usuario


class UserCadastro(Resource):
    """."""

    @jwt_required
    def post(self):
        """."""
        from pymysql.err import IntegrityError
        parser = reqparse.RequestParser()
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


class UserLogin(Resource):
    """."""

    def post(self):
        """."""
        parser = reqparse.RequestParser()
        parser.add_argument('email', help='Email não pode estar vazio!',
                            required=True)
        parser.add_argument('senha', help='Senha não pode estar vazia!',
                            required=True)
        data = parser.parse_args()
        usuario = Usuario(data)
        try:
            usuario = usuario.procurarUsuarioPeloEmail(data['email'])
            if usuario.verify_password('senha', data['senha']):
                access_token = create_access_token(identity=data['email'])
                refresh_token = create_refresh_token(identity=data['email'])
                return {
                    'message': 'Usuario Logado!',
                    'access_token': access_token,
                    'refresh_token': refresh_token
                    }
            else:
                return {'message': 'Credenciais do Usuario Incorretas!'}
        except (AttributeError, ValueError):
            return {'message': 'Usuario não Encontrado!'}
