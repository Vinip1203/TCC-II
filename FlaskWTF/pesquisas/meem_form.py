from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import InputRequired, NumberRange


class FormularioMeem(FlaskForm):


    dia = IntegerField(
        'Que dia é hoje?',
        validators=[
            InputRequired('Informe um valor'),
            NumberRange(min=0, max=1, message='O valor deve estar entre 0 e 1')
    ])

    mes = IntegerField(
        'Em que mês estamos?',
        validators=[
            InputRequired('Informe um valor'),
            NumberRange(min=0, max=1, message='O valor deve estar entre 0 e 1')
    ])

    ano = IntegerField(
        'Em que ano estamos?',
        validators=[
            InputRequired('Informe um valor'),
            NumberRange(min=0, max=1, message='O valor deve estar entre 0 e 1')
    ])

    semana = IntegerField(
        'Em que dia da semana estamos?',
        validators=[
            InputRequired('Informe um valor'),
            NumberRange(min=0, max=1, message='O valor deve estar entre 0 e 1')
    ])

    hora = IntegerField(
        'Qual a hora aproximada?',
        validators=[
            InputRequired('Informe um valor'),
            NumberRange(min=0, max=1, message='O valor deve estar entre 0 e 1')
    ])


    local = IntegerField(
        'Onde estamos agora? (Por exemplo: sala, consultório, quarto...)',
        validators=[
            InputRequired('Informe um valor'),
            NumberRange(min=0, max=1, message='O valor deve estar entre 0 e 1')
    ])

    local_amplo = IntegerField(
        'Em que tipo de lugar estamos? (Por exemplo: hospital, clínica, casa...)',
        validators=[
            InputRequired('Informe um valor'),
            NumberRange(min=0, max=1, message='O valor deve estar entre 0 e 1')
    ])

    bairro = IntegerField(
        'Em que bairro estamos? (Considere o nome de ruas próximas)',
        validators=[
            InputRequired('Informe um valor'),
            NumberRange(min=0, max=1, message='O valor deve estar entre 0 e 1')
    ])

    cidade = IntegerField(
        'Em que cidade nós estamos?',
        validators=[
            InputRequired('Informe um valor'),
            NumberRange(min=0, max=1, message='O valor deve estar entre 0 e 1')
    ])

    estado = IntegerField(
        'Em que estado nós estamos?',
        validators=[
            InputRequired('Informe um valor'),
            NumberRange(min=0, max=1, message='O valor deve estar entre 0 e 1')
    ])


    palavras = IntegerField(
        'Repita as palavras a seguir: vaso, carro, tijolo',
        validators=[
            InputRequired('Informe um valor'),
            NumberRange(min=0, max=3, message='O valor deve estar entre 0 e 3')
    ])

    calculo = IntegerField(
        'Realize subtrações sucessivas de setes: 100-7; 93-7; 86-7; 79-7; 72-7',
        validators=[
            InputRequired('Informe um valor'),
            NumberRange(min=0, max=5, message='O valor deve estar entre 0 e 5')
    ])

    memoria = IntegerField(
        'Lembre-se das três palavras ditas anteriormente',
        validators=[
            InputRequired('Informe um valor'),
            NumberRange(min=0, max=3, message='O valor deve estar entre 0 e 3')
    ])

    objetos = IntegerField(
        'Nomeie corretamente os objetos mostrados: relógio, caneta ',
        validators=[
            InputRequired('Informe um valor'),
            NumberRange(min=0, max=2, message='O valor deve estar entre 0 e 2')
    ])

    repeticao = IntegerField(
        'Repita a frase a seguir: Nem aqui, nem ali, nem lá.',
        validators=[
            InputRequired('Informe um valor'),
            NumberRange(min=0, max=1, message='O valor deve estar entre 0 e 1')
    ])

    comando_verbal = IntegerField(
        'Comando verbal: Pegue esse papel com a mão direita, dobre ao meio e coloque no chão',
        validators=[
            InputRequired('Informe um valor'),
            NumberRange(min=0, max=3, message='O valor deve estar entre 0 e 3')
    ])

    comando_escrito = IntegerField(
        'Leitura de comando escrito: FECHE OS OLHOS',
        validators=[
            InputRequired('Informe um valor'),
            NumberRange(min=0, max=1, message='O valor deve estar entre 0 e 1')
    ])

    escrita = IntegerField(
        'peça ao entrevistado para escrever uma frase que tenha começo, meio e fim',
        validators=[
            InputRequired('Informe um valor'),
            NumberRange(min=0, max=1, message='O valor deve estar entre 0 e 1')
    ])

    desenho = IntegerField(
        'Copia de desenho (dois pentágonos com dois pontos de intersecção)',
        validators=[
            InputRequired('Informe um valor'),
            NumberRange(min=0, max=1, message='O valor deve estar entre 0 e 1')
    ])