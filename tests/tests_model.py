"""."""
from tests_flask_base import TestFlaskBase
from app.models import Model


class TestModel(TestFlaskBase):
    """."""

    def test_model_insere_na_lista_de_atributos_e_inicializador_atualiza_a_lista(self):
        """."""
        esperado = {'test1': 'test', 'test2': 'tset'}
        model = Model()
        model.test1 = 'test'
        model.test2 = 'tset'
        self.assertEqual(str(model), str(esperado))
        # model = Model(esperado)
        # self.assertEqual(str(model), str(esperado))

    def test_representacao_model(self):
        """."""
        esperado = {'test1': 'test', 'test2': 'tset'}
        modelo = Model(esperado)
        self.assertEqual(str(modelo), str(esperado))

    def test_model_verificando_campos_na_lista_de_atributos(self):
        """."""
        model = Model()
        model.test1 = 'test'
        model.test2 = 'tset'
        self.assertEqual(model.test1, 'test')
        self.assertEqual(model.test2, 'tset')

    def test_model_verificando_campos_foram_excluidos_da_lista_de_atributos(self):
        """."""
        esperado = {'test1': 'test', 'test2': 'tset'}
        model = Model()
        model.test1 = 'test'
        model.test2 = 'tset'
        self.assertEqual(str(model), str(esperado))
        self.assertEqual(model.test1, 'test')
        self.assertEqual(model.test2, 'tset')
        del model.test1
        self.assertEqual(str(model), str({'test2': 'tset'}))
        del model.test2
        self.assertEqual(str(model), str({}))

    def test_pk_alterada(self):
        """."""
        esperado = {'test1': 'test', 'test2': 'tset', 'a': 11}
        model = Model(esperado)
        model.setPK('a')
        self.assertEqual(model.__pk__, 'a')
        with self.assertRaises(AttributeError):
            model.setPK('b')
