"""Modulo para preparar o ambiente dos Testes."""
from app import start_app
from unittest import TestCase


class TestFlaskBase(TestCase):
    """Classe Base com as Configurações dos Testes."""

    def setUp(self):
        """Roda antes de todos os testes."""
        self.app = start_app()
        self.app.testing = True
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()
