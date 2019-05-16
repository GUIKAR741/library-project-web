"""."""
from tests_flask_base import TestFlaskBase
from flask import url_for
from unittest.mock import patch


class TestIndexRoute(TestFlaskBase):
    """."""

    def test_se_a_index_retorna_ola(self):
        """."""
        esperado = 'olá'
        retorno = self.client.get(url_for('index.index_route'))
        self.assertEqual(retorno.status_code, 200)
        self.assertEqual(retorno.data.decode(), esperado)

    @patch("app.controllers.render_template", return_value=b'OK')
    def test_pagina_eh_chamado_com_parametro(self, moked):
        """."""
        response = self.client.get(url_for('index.pagina'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'OK')
        moked.assert_called_with('theme/index.html')

    @patch("app.controllers.render_template", return_value=b'OK')
    def test_doc_eh_chamado_com_parametro(self, moked):
        """."""
        response = self.client.get(url_for('index.doc'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'OK')
        moked.assert_called_with('documentation/index.html')
