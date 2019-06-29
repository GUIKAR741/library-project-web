"""Modulo com o Model Usuario."""
from . import Model
from passlib.hash import pbkdf2_sha256


class Usuario(Model):
    """Model da Tabela Usuario."""

    def __init__(self, lista: dict = {}):
        """Inicia o Model."""
        super().__init__(lista)
        self.__table__ = 'usuario'
        self.__pk__ = 'id'

    @property
    def is_authenticated(self):
        """Retorna se o Usuario é Autenticado."""
        return True

    @property
    def is_active(self):
        """Retorna se o Usuario está ativo."""
        return True

    @property
    def is_anonymous(self):
        """Retorna se o Usuario é anonimo."""
        return False

    def get_id(self):
        """Retorna o ID do usuario."""
        return str(self.getDict()[self.__pk__])

    def procurarUsuarioPeloEmail(self, email: str):
        """Verifica se Existe Usuario."""
        usuario = self.select(
            'select * from usuario where email = %(email)s',
            {'email': email}
            )
        return usuario if usuario else None

    def criptografar_senha(self, password):
        """Criptografa Senha."""
        self.__dict__[password] = pbkdf2_sha256.hash(self.__dict__[password])

    def verify_password(self, campoPassword, password):
        """Verifica se a Senha está Correta."""
        return pbkdf2_sha256.verify(password, self.__dict__[campoPassword])
