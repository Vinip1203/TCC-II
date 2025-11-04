from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import InputRequired


class FormularioSarcopenia(FlaskForm):


    forca = RadioField(
        'Qual a dificuldade que você tem para levantar e carregar 4,5kg?',
        choices=[
            ('nenhuma', 'Nenhuma'),
            ('alguma', 'Alguma'),
            ('muita', 'Muita ou impossível')
        ],
        validators=[InputRequired('Selecione uma opção')]
    )


    apoio = RadioField(
        'Qual a dificuldade que tem para atravessar uma sala?',
        choices=[
            ('nenhuma', 'Nenhuma'),
            ('alguma', 'Alguma'),
            ('muita', 'Muita, com apoio ou impossível')
        ],
        validators=[InputRequired('Selecione uma opção')]
    )


    levantar = RadioField(
        'Qual a dificuldade que tem para se levantar de uma cadeira ou de uma cama?',
        choices=[
            ('nenhuma', 'Nenhuma'),
            ('alguma', 'Alguma'),
            ('muita', 'Muita, ou impossível sem ajuda')
        ],
        validators=[InputRequired('Selecione uma opção')]
    )


    escada = RadioField(
        'Qual a dificuldade que tem para subir um lance de 10 degraus?',
        choices=[
            ('nenhuma', 'Nenhuma'),
            ('alguma', 'Alguma'),
            ('muita', 'Muita ou impossível')
        ],
        validators=[InputRequired('Selecione uma opção')]
    )


    quedas = RadioField(
        'Quantas vezes caiu no último ano?',
        choices=[
            ('nenhuma', 'Nenhuma'),
            ('1_a_3', '1 a 3 quedas'),
            ('4_ou_mais', '4 quedas ou mais')
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    submit = SubmitField('Salvar')