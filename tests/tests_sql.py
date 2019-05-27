"""."""
from tests_flask_base import TestFlaskBase
from unittest.mock import patch
from flaskext.mysql import MySQL


class TestQuerys(TestFlaskBase):
    """Teste ."""

    @patch.object(MySQL, "connect")
    def test_query_executa(self, moked):
        """."""
        self.app.db()._query('SELECT * FROM tb_usuario')
        moked().cursor().execute.assert_called_with('SELECT * FROM tb_usuario', None)

    @patch.object(MySQL, "connect")
    def test_se_o_select_foi_chamado(self, moked):
        """."""
        self.app.db().select('SELECT * FROM tb_usuario')
        moked().cursor().execute.assert_called_with('SELECT * FROM tb_usuario', None)
        moked().cursor().fetchone.assert_called()

    @patch.object(MySQL, "connect")
    def test_se_o_select_foi_chamado_com_fetchall(self, moked):
        """."""
        self.app.db().select('SELECT * FROM mysql.user', None, 'fetchall')
        moked().cursor().execute.assert_called_with(
            'SELECT * FROM mysql.user', None)
        moked().cursor().fetchall.assert_called()

    def test_se_o_select_em_uma_tabela_que_nao_existe_gera_excecao(self):
        """."""
        import pymysql
        with self.assertRaises(pymysql.err.ProgrammingError):
            self.app.db().select('SELECT * FROM a', None)

    def test_se_o_select_de_valor_que_nao_existe_retorna_vazio(self):
        """."""
        self.assertEqual(
            self.app.db().select(
                'SELECT * FROM usuario WHERE id = %(id)s', {'id': -1}
                ),
            None
            )
        self.assertEqual(
            self.app.db().select(
                'SELECT * FROM usuario where id= %(id)s', {'id': -1}, 'fetchall'
                ),
            ()
            )

    @patch.object(MySQL, "connect")
    def test_operacao_insert_esta_sendo_chamado_certo(self, moked):
        """."""
        self.app.db().operacao(
            'insert into Livro values'
            '(null, %(nome)s, %(autor)s, %(editora)s, %(capa)s, %(ano)s, %(idioma)s, %(isbn)s)',
            {'nome': 'livro',
             'autor': 'autor',
             'editora': 'editora',
             'capa': 'capa',
             'ano': 2000,
             'idioma': 'portugues',
             'isbn': '23456734567'})
        moked().cursor().execute.assert_called_with(
            'insert into Livro values'
            '(null, %(nome)s, %(autor)s, %(editora)s, %(capa)s, %(ano)s, %(idioma)s, %(isbn)s)',
            {'nome': 'livro',
             'autor': 'autor',
             'editora': 'editora',
             'capa': 'capa',
             'ano': 2000,
             'idioma': 'portugues',
             'isbn': '23456734567'}
        )
        moked().commit.assert_called()

    @patch.object(MySQL, "connect")
    def test_operacao_update_esta_sendo_chamado_certo(self, moked):
        """."""
        self.app.db().operacao(
            'UPDATE Livro SET '
            'nome = %(nome)s,  autor = %(autor)s, editora = %(editora)s, '
            'capa = %(capa)s, ano = %(ano)s, idioma = %(idioma)s, isbn = %(isbn)s '
            'WHERE id = %(id)s',
            {'id': 1,
             'nome': 'livro1',
             'autor': 'autor1',
             'editora': 'editora1',
             'capa': 'capa1',
             'ano': 2001,
             'idioma': 'portugues1',
             'isbn': '2345673456'})
        moked().cursor().execute.assert_called_with(
            'UPDATE Livro SET '
            'nome = %(nome)s,  autor = %(autor)s, editora = %(editora)s, '
            'capa = %(capa)s, ano = %(ano)s, idioma = %(idioma)s, isbn = %(isbn)s '
            'WHERE id = %(id)s',
            {'id': 1,
             'nome': 'livro1',
             'autor': 'autor1',
             'editora': 'editora1',
             'capa': 'capa1',
             'ano': 2001,
             'idioma': 'portugues1',
             'isbn': '2345673456'}
        )
        moked().commit.assert_called()

    @patch.object(MySQL, "connect")
    def test_operacao_delete_esta_sendo_chamado_certo(self, moked):
        """."""
        self.app.db().operacao(
            'DELETE FROM Livro WHERE id = %(id)s ',
            {'id': 1}
        )
        moked().cursor().execute.assert_called_with(
            'DELETE FROM Livro WHERE id = %(id)s ',
            {'id': 1}
        )
        moked().commit.assert_called()
