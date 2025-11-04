from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import InputRequired


class NovaPesquisaForm(FlaskForm):
    nome_entrevistado = StringField('Nome do entrevistado', validators=[
        InputRequired('Por favor, insira o nome do entrevistado.')
    ])
    tipo_estudo = SelectField(
        'Tipo de estudo',
        choices=[
            ('', 'Selecione uma opção...'),
            ('coorte', 'Estudo de Coorte'),
            ('vida_saude', 'Condições de Vida e Saúde das Populações Idosas (Morais 2007)'),
            ('meem', 'Mini-exame de estado mental (MEEM)'),
            ('ansiedade', 'Inventário de ansiedade geriátrica (GAI)'),
            ('qual_vida', 'Questionário de avaliação da qualidade de vida (SF-36)'),
            ('alimentacao', 'Como ter uma alimentação saudável (Ministério da Saúde)'),
            ('atv_fisica', 'Questionário internacional de atividade física (versão curta)'),
            ('sarcopenia', 'Ferramenta de rastreio do risco de sarcopenia (SARC-F)')
        ],
        validators=[InputRequired('Por favor, selecione um tipo de estudo.')])

    submit = SubmitField('Iniciar')
