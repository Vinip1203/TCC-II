from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[
        InputRequired('Informe seu endereço de e-email.'),
        Email('Formato de e-mail inválido.')
    ])
    senha = PasswordField('Senha', validators=[
        InputRequired('Informe sua senha.')
    ])
    remember_me = BooleanField('Permanecer conectado')
    submit = SubmitField('Entrar')


class EsqueceuForm(FlaskForm):
    email = StringField('E-mail', validators=[
        InputRequired('Informe seu endereço de e-email.'),
        Email('Formato de e-mail inválido.')
    ])
    submit = SubmitField('Enviar')


class RedefinirForm(FlaskForm):
    nova_senha = PasswordField('Nova senha', validators=[
        InputRequired('A nova senha não pode ser vazia.')
    ])
    confirmar_senha = PasswordField('Confirmar nova senha', validators =[
        InputRequired('Por favor, confirme sua nova senha.'),
        EqualTo('nova_senha', message='As senhas não coincidem.')
    ])
    submit = SubmitField('Redefinir senha')