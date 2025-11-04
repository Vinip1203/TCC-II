from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SubmitField
from wtforms.validators import InputRequired, Email


class CadastroForm(FlaskForm):
    nome_usuario = StringField('Nome', validators=[
        InputRequired('Informe um nome de usuário')
    ])
    email = StringField('E-mail', validators=[
        InputRequired('Informe um endereço de e-email.'),
        Email('Formato de e-mail inválido.')
    ])
    senha = PasswordField('Senha', validators=[
        InputRequired('Informe uma senha.')
    ])
    papel = RadioField('Papel', choices=[('Administrador', 'Administrador'), ('Pesquisador', 'Pesquisador')], validators=[
        InputRequired('Selecione um papel de usuário')
    ])
    submit = SubmitField('Cadastrar')