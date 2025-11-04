from flask_wtf import FlaskForm
from wtforms import RadioField, SelectMultipleField, IntegerField, SubmitField
from wtforms.validators import InputRequired, NumberRange
from wtforms import widgets


class FormularioAlimentacao(FlaskForm):
    

    qtd_frutas = RadioField(
        'Quantas frutas você consome diariamente?',
        choices=[
            ('nao_come', 'Não como frutas'),
            ('3_ou_mais', '3 ou mais unidades'),
            ('2_unidades', '2 unidades'),
            ('1_unidade', '1 unidade')
        ],
        validators=[InputRequired('Selecione uma opção')]
    )
    
  
    qtd_verduras = RadioField(
        'Quantos legumes e verduras você come por dia?',
        choices=[
            ('nao_come', 'Não consumo verduras e legumes'),
            ('3_ou_menos', '3 ou menos colheres de sopa'),
            ('4_a_5', '4 a 5 colheres de sopa'),
            ('6_a_7', '6 a 7 colheres de sopa'),
            ('8_ou_mais', '8 ou mais colheres de sopa')
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    
    qtd_leguminosas = RadioField(
        'Com que frequência você consome leguminosas, sementes ou castanhas?',
        choices=[
            ('nao_consome', 'Não consumo'),
            ('2_ou_mais', '2 ou mais colheres de sopa por dia'),
            ('menos_5_vezes', 'Menos de 5 vezes por semana'),
            ('1_ou_menos', '1 colher de sopa ou menos por dia')
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    # 4 - Quantidade carboidratos
    qtd_carbo = IntegerField(
        'Carboidratos:',
        validators=[
            InputRequired('Informe uma quantidade'),
            NumberRange(min=0, max=50, message='A quantidade deve ser um número inteiro')
    ])
    
    qtd_pao = IntegerField(
        'Pães:',
        validators=[
            InputRequired('Informe uma quantidade'),
            NumberRange(min=0, max=50, message='A quantidade deve ser um número inteiro')
    ])

    qtd_bolo = IntegerField(
        'Bolos:',
        validators=[
            InputRequired('Informe uma quantidade'),
            NumberRange(min=0, max=50, message='A quantidade deve ser um número inteiro')
    ])

    qtd_bolacha = IntegerField(
        'Biscoitos:',
        validators=[
            InputRequired('Informe uma quantidade'),
            NumberRange(min=0, max=50, message='A quantidade deve ser um número inteiro')
    ])

    

    qtd_carnes = RadioField(
        'Com que frequência você consome carnes ou ovos?',
        choices=[
            ('nao_consome', 'Não consumo'),
            ('1_porcao', '1 porção ou 1 ovo por dia'),
            ('2_porcoes', '2 porções ou 2 ovos por dia'),
            ('mais_de_2', 'Mais de 2 porções ou ovos por dia')
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    

    gordura_carne = RadioField(
        'Você retira a gordura das carnes ou a pele do frango?',
        choices=[
            ('sim', 'Sim'),
            ('nao', 'Não'),
            ('nao_come', 'Não como carne vermelha ou frango')
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    
    qtd_peixes = RadioField(
        'Com que frequência você consome peixes?',
        choices=[
            ('nao_consome', 'Não consumo'),
            ('algumas_vezes_ano', 'Somente algumas vezes no ano'),
            ('2_ou_mais_semana', '2 ou mais vezes por semana'),
            ('1_a_4_mes', 'De 1 a 4 vezes por mês')
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    
    qtd_laticinios = RadioField(
        'Qual é, em média, a quantidade de leite e derivados que você come por dia?',
        choices=[
            ('nao_consome', 'Não consumo leite nem derivados'),
            ('3_ou_mais', '3 ou mais porções'),
            ('2_copos', '2 porções'),
            ('1_ou_menos', '1 ou menos porções')
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    
    tipo_laticinios = RadioField(
        'Que tipo de leite e seus derivados você habitualmente consome?',
        choices=[
            ('nao_consome', 'Não consumo leite nem derivados'),
            ('integral', 'Integral'),
            ('baixo_gordura', 'Com baixo teor de gorduras (semidesnatado, desnatado ou light)')
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    
    qtd_processados = RadioField(
        'Com que frequência você consome alimentos processados?',
        choices=[
            ('raramente', 'Raramente ou nunca'),
            ('todos_dias', 'Todos os dias'),
            ('2_a_3_semana', 'De 2 a 3 vezes por semana'),
            ('4_a_5_semana', 'De 4 a 5 vezes por semana'),
            ('menos_2_semana', 'Menos que 2 vezes por semana')
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    
    qtd_doces = RadioField(
        'Com que frequência você consome doces e bebidas industrializadas?',
        choices=[
            ('raramente', 'Raramente ou nunca'),
            ('menos_2_semana', 'Menos que 2 vezes por semana'),
            ('2_a_3_semana', 'De 2 a 3 vezes por semana'),
            ('4_a_5_semana', 'De 4 a 5 vezes por semana'),
            ('todos_dias', 'Todos os dias')
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    
    tipo_gordura = RadioField(
        'Qual tipo de gordura você mais utiliza para cozinhar?',
        choices=[
            ('banha_manteiga', 'Banha animal ou manteiga'),
            ('oleo_vegetal', 'Óleo vegetal'),
            ('margarina_gordura', 'Margarina ou gordura vegetal')
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    
    sal = RadioField(
        'Você costuma adicionar sal aos alimentos após servi-los?',
        choices=[
            ('sim', 'Sim'),
            ('nao', 'Não')
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

   
    refeicoes_diarias = SelectMultipleField(
        'Quais refeições você costuma fazer habitualmente no dia?',
        choices=[
            ('cafe_manha', 'Café da manhã'),
            ('lanche_manha', 'Lanche da manhã'),
            ('almoco', 'Almoço'),
            ('lanche_tarde', 'Lanche da tarde'),
            ('jantar', 'Jantar'),
            ('lanche_noite', 'Lanche antes de dormir')
        ],
        validators=[InputRequired('Selecione uma ou mais opções')],
        option_widget=widgets.CheckboxInput(), # Renderiza cada uma das opções como checkbox
        widget=widgets.ListWidget(prefix_label=False) # Remove o rótulo principal do campo e renderiza refeicoes_diarias como uma lista
    )

    
    qtd_agua = RadioField(
        'Em média, quantos copos de água, sucos ou chás você bebe diariamente?',
        choices=[
            ('menos_4', 'Menos de 4 copos'),
            ('8_ou_mais', '8 copos ou mais'),
            ('4_a_5', '4 a 5 copos'),
            ('6_a_8', '6 a 8 copos')
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    
    qtd_alcool = RadioField(
        'Você costuma consumir bebidas alcoólicas com que frequência?',
        choices=[
            ('diariamente', 'Diariamente'),
            ('1_a_6_semana', '1 a 6 vezes por semana'),
            ('eventualmente', 'Eventualmente ou raramente'),
            ('nao_consome', 'Não consumo')
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

   
    atv_fisica = RadioField(
        'Você costuma fazer atividade física regularmente (30 minutos diários)?',
        choices=[
            ('nao', 'Não'),
            ('sim', 'Sim'),
            ('2_a_4_semana', '2 a 4 vezes por semana')
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

   
    info_nutri = RadioField(
        'Você lê as informações nutricionais dos alimentos antes de comprá-los?',
        choices=[
            ('nunca', 'Nunca'),
            ('quase_nunca', 'Quase nunca'),
            ('algumas_vezes', 'Algumas vezes, para alguns produtos'),
            ('sempre', 'Sempre ou quase sempre, para todos os produtos')
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    submit = SubmitField('Salvar') 