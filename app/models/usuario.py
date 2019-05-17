"""."""
from . import Model
from passlib.hash import pbkdf2_sha256


class Usuario(Model):
    """Model da Tabela ."""

    __table__ = 'usuario'

    def procurarUsuarioPeloEmail(self, email: str):
        """."""
        usuario = self.select(
            'select * from usuario where email = %(email)s',
            {'email': email}
            )
        if usuario:
            return usuario

    def criptografar_senha(self, password):
        """."""
        self.__setattr__(password, pbkdf2_sha256.hash(self.__getattr__(password)))

    def verify_password(self, password):
        """."""
        return pbkdf2_sha256.verify(password, self.__getattr__(password))
