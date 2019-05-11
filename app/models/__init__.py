"""Model Base do Banco."""
from flask import current_app
from flaskext.mysql import MySQL

mysql = MySQL()


def configure(app):
    """."""
    mysql.init_app(app)
    app.db = mysql


class sql:
    """Classe para Executar Comandos SQL."""

    def __init__(self):
        """
        Metodo Inicializador da Classe SQL.

        Abre a Conexão
        """
        self.conn = current_app.db.connect()

    def __del__(self):
        """
        Metodo Destrutor da Classe SQL.

        Fecha a Conexão
        """
        self.conn.close()

    def query(self, sql, campos=None):
        """Executa as Querys."""
        with self.conn() as curr:
            curr.execute(sql, campos)
            res = curr
        return res

    def select(self, sql, campos=None, sel='fetchone'):
        """Executa Select no Banco de Dados."""
        with self.conn.cursor() as curr:
            curr.execute(sql, campos)
            if sel == 'fetchone':
                sel = curr.fetchone()
            if sel == 'fetchall':
                sel = curr.fetchall()
        return sel
