"""."""
from tests_flask_base import TestFlaskBase
from flask import url_for


class TestAPI(TestFlaskBase):
    """."""

    def test_api_rota_user_cadastro(self):
        """."""
        self.client.post(url_for('api.userCadastro'), json={'email': 'gui@gmail.com'})
