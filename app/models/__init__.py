"""Model Base do Banco."""
from app import mysql


class sql:
    """Classe para Executar Comandos SQL."""

    def __init__(self):
        """Metodo Inicializador da Classe SQL."""
        self.conn = mysql.connect()

    def query(self, sql, campos=None):
        """Executa as Querys."""
        with self.conn.cursor() as curr:
            curr.execute(sql, campos)
            res = curr
        return res
