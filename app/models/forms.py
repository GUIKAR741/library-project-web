"""Modulo com Formularios do Site."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """Formulario de Login."""

    usuario = StringField("Usuario", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired()])


class UserForm(FlaskForm):
    """Formulario do Perfil do Usuario."""

    nome = StringField("Usuario", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    cpf = StringField("CPF")
    telefone = StringField("Telefone")
    senha = PasswordField("Senha", validators=[DataRequired()])
    novaSenha = PasswordField("Nova Senha")
    confNovaSenha = PasswordField("Confirmar Nova Senha")
