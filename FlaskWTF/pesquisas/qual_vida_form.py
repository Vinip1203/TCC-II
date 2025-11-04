from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import InputRequired


opcoes_resposta = [
    ('Verdadeiro', 'Definitivamente verdadeiro'),
    ('Vezes_verdadeiro', 'A maioria das vezes verdadeiro'),
    ('Nao_sei', 'Nao sei'),
    ('Vezes_falso', 'A maioria das vezes falso'),
    ('Falso', 'Definitivamente falso'),
]


opcoes_resposta_2 = [
    ('Dificulta_muito', 'Sim, Dificulta muito'),
    ('Dificulta_pouco', 'Sim, dificulta um pouco'),
    ('Nao_dificulta', 'Não dificulta de modo algum')
]


opcoes_resposta_3 = [
    ('Todo_tempo', 'Todo tempo'),
    ('Maior_parte', 'A maior parte do tempo'),
    ('Boa_parte', 'Uma boa parte do tempo'),
    ('Alguma_parte', 'Alguma parte do tempo'),
    ('Pequena_parte', 'Uma pequena parte do tempo'),
    ('Nunca', 'Nunca')
]


opcoes_resposta_4 = [
    ('Sim', 'Sim'),
    ('Nao', 'Não')
]


class FormularioQualidadeVida(FlaskForm):
    

    # QUALIDADE DE VIDA GERAL
    saude_geral = RadioField(
        'Em geral você diria que sua saúde é: ',
        choices=[
            ('Excelente', 'Excelente'),
            ('Muito_boa', 'Muito boa'),
            ('Boa', 'Boa'),
            ('Ruim', 'Ruim'),
            ('Muito_ruim', 'Muito ruim'),
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    idade = RadioField(
        'Comparada há um ano atrás, como você classificaria sua idade agora? ',
        choices=[
            ('Muito_melhor', 'Muito melhor'),
            ('Pouco_melhor', 'Um pouco melhor'),
            ('Mesma', 'Quase a mesma'),
            ('Pouco_pior', 'Um pouco pior'),
            ('Muito_pior', 'Muito pior'),
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    obediencia = RadioField(
        'Eu costumo obedecer um pouco mais facilmente que as outras pessoas',
        choices=opcoes_resposta,
        validators=[InputRequired('Selecione uma opção')]
    )

    saudavel = RadioField(
        'Eu sou tão saudável quanto qualquer pessoa que eu conheço',
        choices=opcoes_resposta,
        validators=[InputRequired('Selecione uma opção')]
    )

    saude_pior = RadioField(
        'Eu acho que minha saúde vai piorar',
        choices=opcoes_resposta,
        validators=[InputRequired('Selecione uma opção')]
    )

    avl_saude = RadioField(
        'Minha saúde é excelente',
        choices=opcoes_resposta,
        validators=[InputRequired('Selecione uma opção')]
    )


    # QUALIDADE DE VIDA ATV FISICA
    atv_rigorosa = RadioField(
        'Atividades rigorosas',
        choices=opcoes_resposta_2,
        validators=[InputRequired('Selecione uma opção')]
    )

    atv_moderada = RadioField(
        'Atividades moderadas',
        choices=opcoes_resposta_2,
        validators=[InputRequired('Selecione uma opção')]
    )

    carregar_mant = RadioField(
        'Levantar ou carregar mantimentos',
        choices=opcoes_resposta_2,
        validators=[InputRequired('Selecione uma opção')]
    )

    subir_lance = RadioField(
        'Subir vários lances de escada',
        choices=opcoes_resposta_2,
        validators=[InputRequired('Selecione uma opção')]
    )

    subir_escada = RadioField(
        'Subir um lance de escada',
        choices=opcoes_resposta_2,
        validators=[InputRequired('Selecione uma opção')]
    )

    flexionar = RadioField(
        'Curvar-se, ajoelhar-se ou dobrar-se',
        choices=opcoes_resposta_2,
        validators=[InputRequired('Selecione uma opção')]
    )

    andar_1km = RadioField(
        'Andar mais de 1 quilômetro',
        choices=opcoes_resposta_2,
        validators=[InputRequired('Selecione uma opção')]
    )

    andar_quart = RadioField(
        'Andar um quarteirão',
        choices=opcoes_resposta_2,
        validators=[InputRequired('Selecione uma opção')]
    )

    andar_vq = RadioField(
        'Andar vários quarteirões',
        choices=opcoes_resposta_2,
        validators=[InputRequired('Selecione uma opção')]
    )

    banho = RadioField(
        'Tomar banho ou vestir-se',
        choices=opcoes_resposta_2,
        validators=[InputRequired('Selecione uma opção')]
    )

    dor_corpo = RadioField(
        'Quanta dor no corpo você teve durante as últimas 4 semanas? ',
        choices=[
            ('Nenhuma', 'Nenhuma'),
            ('Muito_leve', 'Muito leve'),
            ('Leve', 'Leve'),
            ('Moderada', 'Moderada'),
            ('Grave', 'Grave'),
            ('Muito_grave', 'Muito grave'),
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    dor_afetou = RadioField(
        'Durante as últimas 4 semanas, quanto a dor interferiu no seu trabalho e tarefas domésticas? ',
        choices=[
            ('Nao_afetou', 'De maneira alguma'),
            ('Pouco', 'Um pouco'),
            ('Moderadamente', 'Moderadamente'),
            ('Bastante', 'Bastante'),
            ('Extremamente', 'Extremamente'),
        ],
        validators=[InputRequired('Selecione uma opção')]
    )


    # QUALIDADE DE VIDA EMOCIONAL
    vigor = RadioField(
        'Quanto tempo você tem se sentido cheio de vigor, vontade ou força? ',
        choices=opcoes_resposta_3,
        validators=[InputRequired('Selecione uma opção')]
    )

    nervoso = RadioField(
        'Quanto tempo você tem se sentido nervoso? ',
        choices=opcoes_resposta_3,
        validators=[InputRequired('Selecione uma opção')]
    )

    deprimido = RadioField(
        'Quanto tempo você tem se sentido deprimido? ',
        choices=opcoes_resposta_3,
        validators=[InputRequired('Selecione uma opção')]
    )

    calmo = RadioField(
        'Quanto tempo você tem se sentido calmo ou tranquilo? ',
        choices=opcoes_resposta_3,
        validators=[InputRequired('Selecione uma opção')]
    )

    energia = RadioField(
        'Quanto tempo você tem se sentido cheio de energia? ',
        choices=opcoes_resposta_3,
        validators=[InputRequired('Selecione uma opção')]
    )

    desanimado = RadioField(
        'Quanto tempo você tem se sentido desanimado ou abatido? ',
        choices=opcoes_resposta_3,
        validators=[InputRequired('Selecione uma opção')]
    )

    esgotado = RadioField(
        'Quanto tempo você tem se sentido esgotado? ',
        choices=opcoes_resposta_3,
        validators=[InputRequired('Selecione uma opção')]
    )

    feliz = RadioField(
        'Quanto tempo você tem se sentido feliz? ',
        choices=opcoes_resposta_3,
        validators=[InputRequired('Selecione uma opção')]
    )

    cansado = RadioField(
        'Quanto tempo você tem se sentido cansado? ',
        choices=opcoes_resposta_3,
        validators=[InputRequired('Selecione uma opção')]
    )


    # QUALIDADE DE VIDA LIMITAÇÕES
    temp_atv_fis = RadioField(
        'Você diminui a quantidade de tempo que se dedicava ao seu trabalho ou a outras atividades? ',
        choices=opcoes_resposta_4,
        validators=[InputRequired('Selecione uma opção')]
    )

    qtd_atv_fis = RadioField(
        'Realizou menos tarefas do que você gostaria? ',
        choices=opcoes_resposta_4,
        validators=[InputRequired('Selecione uma opção')]
    )

    limitado_fis = RadioField(
        'Esteve limitado no seu tipo de trabalho ou a outras atividades?',
        choices=opcoes_resposta_4,
        validators=[InputRequired('Selecione uma opção')]
    )

    dif_fis = RadioField(
        'Teve dificuldades ou necessitou de um esforço extra ao realizar seu trabalho ou outras atividades?',
        choices=opcoes_resposta_4,
        validators=[InputRequired('Selecione uma opção')]
    )

    temp_atv_emo = RadioField(
        'Você diminui a quantidade de tempo que se dedicava ao seu trabalho ou a outras atividades? ',
        choices=opcoes_resposta_4,
        validators=[InputRequired('Selecione uma opção')]
    )

    qtd_atv_emo = RadioField(
        'Realizou menos tarefas do que você gostaria? ',
        choices=opcoes_resposta_4,
        validators=[InputRequired('Selecione uma opção')]
    )

    cuidado_atv = RadioField(
        'Não realizou ou fez qualquer das atividades com tanto cuidado como geralmente faz? ',
        choices=opcoes_resposta_4,
        validators=[InputRequired('Selecione uma opção')]
    )

    social = RadioField(
        'Durante as últimas 4 semanas, de que maneira sua saúde física ou problemas emocionais interferiram nas suas atividades sociais normais, em relação à família, amigos ou em grupo?',
        choices=[
            ('Nenhuma', 'De forma nenhuma'),
            ('Ligeiramente', 'Ligeiramente'),
            ('Moderadamente', 'Moderadamente'),
            ('Bastante', 'Bastante'),
            ('Extremamente', 'Extremamente')
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    temp_social = RadioField(
        'Durante as últimas 4 semanas, quanto de seu tempo a sua saúde física ou problemas emocionais interferiram com as atividades sociais?',
        choices=[
            ('Todo_tempo', 'Todo tempo'),
            ('Maior_parte', 'Maior parte do tempo'),
            ('Alguma_parte', 'Alguma parte do tempo'),
            ('Pequena_parte', 'Uma pequena parte do tempo'),
            ('Nenhuma', 'Nenhuma parte do tempo')
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    submit = SubmitField('Salvar')