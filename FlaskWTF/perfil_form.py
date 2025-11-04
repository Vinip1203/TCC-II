from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, Optional


class PerfilForm(FlaskForm):
    novo_email = StringField('E-mail', validators=[Email('Formato de e-mail inválido.'), Optional()])
    senha_atual = PasswordField('Senha atual', validators=[Optional()])
    nova_senha = PasswordField('Nova senha', validators=[Optional()])
    confirmar_senha = PasswordField('Confirmar nova senha', validators=[Optional()])
    submit = SubmitField('Atualizar')