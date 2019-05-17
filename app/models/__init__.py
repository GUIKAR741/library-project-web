"""Model Base do Banco."""
from flask import current_app
from flaskext.mysql import MySQL

mysql = MySQL()


def configure(app):
    """Registra o mysql no flask."""
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
        self.rows = None

    def __del__(self):
        """
        Metodo Destrutor da Classe SQL.

        Fecha a Conexão
        """
        self.conn.close()

    def _query(self, sql: str, campos: str = None):
        """Executa as Querys."""
        cursor = self.conn.cursor()
        self.rows = cursor.execute(sql, campos)
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
        self.conn.commit()
        return self.rows


class Model:
    """Classe de Model para Interface com o Banco."""

    __table__ = None
    _lista = {}
    _pk = None

    def __init__(self, lista: dict = {}):
        """Metodo Inicializador da Classe."""
        for i in lista.items():
            self.__setattr__(i[0], i[1])

    def __getattr__(self, name):
        """Metodo para pegar valores na lista."""
        return self._lista[name]

    def __setattr__(self, name, value):
        """Metodo para colocar valores na lista."""
        self._lista[name] = value

    def __delattr__(self, name):
        """Metodo para deletar valores da lista."""
        del self._lista[name]

    def __repr__(self):
        """Representação do Objeto."""
        return str(self._lista)

    @classmethod
    def setPK(cls, campo):
        """Metodo para escolhar a chave primaria da tabela."""
        if campo in cls._lista.keys():
            cls._pk = campo
        else:
            raise AttributeError('Campo Não Definido na Tabela')

    def insert(self):
        """Insere os dados na tabela com os campos adicionados."""
        campos = ", ".join(self._lista.keys())
        values = ", ".join(map(lambda x: f"%({x})s", self._lista.keys()))
        return current_app.db().operacao(
            f"INSERT INTO {self.__table__}({campos}) VALUES ({values})",
            self._lista
        )

    def update(self, campo, val):
        """Atualiza os campos da tabela."""
        campos = ', '.join(
            map(lambda x: ' = '.join(x),
                zip(
                    filter(
                        lambda x: not (self._pk == x),
                        self._lista.keys()
                    ),
                    map(lambda x: f"%({x})s",
                        filter(
                            lambda x: not (self._pk == x),
                            self._lista.keys()
                            )
                        )
                    )
                )
            )
        values = dict(self._lista)
        values[campo] = val
        return current_app.db().operacao(
            f"UPDATE {self.__table__} "
            f"SET {campos} where {campo} = %({campo})s",
            values
        )

    def delete(self, campo, val):
        """Remove o registro da Tabela."""
        return current_app.db().operacao(
            f"DELETE FROM {self.__table__} WHERE {campo} = %({campo})s",
            {campo: val}
        )

    def select(self, sql, campos=None, sel='fetchone'):
        """Seleciona Registros da Tabela."""
        if sel == 'fetchone':
            model = self.__class__()
            items = current_app.db().select(sql, campos, sel)
            if items:
                for x in items.items():
                    model.__setattr__(x[0], x[1])
        elif sel == 'fetchall':
            model = current_app.db().select(sql, campos, sel)
        return model
