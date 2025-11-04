from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import InputRequired


opcoes_resposta = [
    ('concordo', 'Concordo'),
    ('discordo', 'Discordo')
]


class FormularioAnsiedade(FlaskForm):


    p1 = RadioField(
        'Ando preocupado(a) a maior parte do tempo',
        choices=opcoes_resposta,
        validators=[InputRequired('Selecione uma opção')]
    )


    p2 = RadioField(
        'Tenho dificuldades em tomar decisões',
        choices=opcoes_resposta,
        validators=[InputRequired('Selecione uma opção')]
    )


    p3 = RadioField(
        'Sinto-me inquieto(a) muitas vezes',
        choices=opcoes_resposta,
        validators=[InputRequired('Selecione uma opção')]
    )


    p4 = RadioField(
        'Tenho dificuldade em relaxar',
        choices=opcoes_resposta,
        validators=[InputRequired('Selecione uma opção')]
    )


    p5 = RadioField(
        'Não consigo apreciar as coisas por causa das minhas preocupações',
        choices=opcoes_resposta,
        validators=[InputRequired('Selecione uma opção')]
    )


    p6 = RadioField(
        'Coisas sem importância preocupam-me bastante',
        choices=opcoes_resposta,
        validators=[InputRequired('Selecione uma opção')]
    )


    p7 = RadioField(
        'Sinto muitas vezes um aperto no estômago',
        choices=opcoes_resposta,
        validators=[InputRequired('Selecione uma opção')]
    )


    p8 = RadioField(
        'Vejo-me como uma pessoa preocupada',
        choices=opcoes_resposta,
        validators=[InputRequired('Selecione uma opção')]
    )


    p9 = RadioField(
        'Não consigo evitar preocupar-me, mesmo com coisas menores',
        choices=opcoes_resposta,
        validators=[InputRequired('Selecione uma opção')]
    )


    p10 = RadioField(
        'Sinto-me muitas vezes nervoso(a)',
        choices=opcoes_resposta,
        validators=[InputRequired('Selecione uma opção')]
    )


    p11 = RadioField(
        'Muitas vezes os meus próprios pensamentos põem-me ansioso(a)',
        choices=opcoes_resposta,
        validators=[InputRequired('Selecione uma opção')]
    )


    p12 = RadioField(
        'Fico com o estômago às voltas devido à minha preocupação constante',
        choices=opcoes_resposta,
        validators=[InputRequired('Selecione uma opção')]
    )


    p13 = RadioField(
        'Vejo-me como uma pessoa nervosa',
        choices=opcoes_resposta,
        validators=[InputRequired('Selecione uma opção')]
    )


    p14 = RadioField(
        'Estou sempre à espera que aconteça o pior',
        choices=opcoes_resposta,
        validators=[InputRequired('Selecione uma opção')]
    )


    p15 = RadioField(
        'Muitas vezes sinto-me agitado(a) interiormente',
        choices=opcoes_resposta,
        validators=[InputRequired('Selecione uma opção')]
    )


    p16 = RadioField(
        'Acho que as minhas preocupações interferem com a minha vida',
        choices=opcoes_resposta,
        validators=[InputRequired('Selecione uma opção')]
    )


    p17 = RadioField(
        'Muitas vezes sou dominado(a) pelas minhas preocupações',
        choices=opcoes_resposta,
        validators=[InputRequired('Selecione uma opção')]
    )


    p18 = RadioField(
        'Por vezes sinto um nó grande no estômago',
        choices=opcoes_resposta,
        validators=[InputRequired('Selecione uma opção')]
    )


    p19 = RadioField(
        'Deixo de me envolver nas coisas por me preocupar demasiado',
        choices=opcoes_resposta,
        validators=[InputRequired('Selecione uma opção')]
    )


    p20 = RadioField(
        'Muitas vezes sinto-me aflito(a)',
        choices=opcoes_resposta,
        validators=[InputRequired('Selecione uma opção')]
    )


    submit = SubmitField('Salvar')