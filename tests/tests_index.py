"""."""
from tests_flask_base import TestFlaskBase
from flask import url_for


class TestIndexRoute(TestFlaskBase):
    """."""

    def test_se_a_index_retorna_ola(self):
        """."""
        esperado = 'olá'
        retorno = self.client.get(url_for('index.index_route'))
        self.assertEqual(retorno.data.decode(), esperado)
