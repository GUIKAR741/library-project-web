"""Model Base do Banco."""
from flaskext.mysql import MySQL

mysql = MySQL()


def configure(app):
    """."""
    mysql.init_app(app)
    app.db = sql


class sql:
    """Classe para Executar Comandos SQL."""

    def __init__(self):
        """
        Metodo Inicializador da Classe SQL.

        Abre a Conexão
        """
        self.conn = mysql.connect()

    def __del__(self):
        """
        Metodo Destrutor da Classe SQL.

        Fecha a Conexão
        """
        self.conn.close()

    def _query(self, sql, campos=None):
        """Executa as Querys."""
        cursor = self.conn.cursor()
        cursor.execute(sql, campos)
        return cursor

    def select(self, sql, campos=None, sel='fetchone'):
        """Executa Select no Banco de Dados."""
        curr = self._query(sql, campos)
        if sel == 'fetchone':
            sel = curr.fetchone()
        if sel == 'fetchall':
            sel = curr.fetchall()
        return sel

    def operacao(self, sql, campos=None):
        """Executa Select no Banco de Dados."""
        self._query(sql, campos)
        return self.conn.commit()


class Model:
    """Classe de Model para Interface com o Banco."""

    _lista = {}

    def __getattr__(self, name):
        """Metodo para pegar valores na lista."""
        return self._lista[name]

    def __setattr__(self, name, value):
        """Metodo para colocar valores na lista."""
        self._lista[name] = value

    def __delattr__(self, name):
        """Metodo para deletar valores da lista."""
        del self._lista[name]
