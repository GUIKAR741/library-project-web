"""."""
from tests_flask_base import TestFlaskBase
from flask import url_for
from unittest.mock import patch


class TestIndexRoute(TestFlaskBase):
    """."""

    def test_login_status_200(self):
        """."""
        retorno = self.client.get(url_for('index.login'))
        self.assertEqual(retorno.status_code, 200)

    def test_esqueceu_senha_status_200(self):
        """."""
        retorno = self.client.get(url_for('index.senha'))
        self.assertEqual(retorno.status_code, 200)

    def test_erro_404(self):
        """."""
        retorno = self.client.get('/test404')
        self.assertEqual(retorno.status_code, 404)

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
