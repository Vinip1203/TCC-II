from flask_wtf import FlaskForm
from wtforms import RadioField, SelectMultipleField, SubmitField, DateField, StringField, IntegerField
from wtforms.validators import InputRequired, Optional
from wtforms import widgets


opcoes_resposta = [
    ('Nao_tem', 'Não tem'),
    ('Tem_nao_interfere', 'Tem, não interfere'),
    ('Tem_interfere', 'Tem e interfere'),
]


class FormularioVidaSaude(FlaskForm):
    

    # INFORMAÇÕES PESSOAIS
    data_nasc = DateField(
        'Data de nascimento',
        validators=[InputRequired('Selecione uma opção')]
    )

    sexo = RadioField(
        'Sexo',
        choices=[
            ('M', 'Masculino'),
            ('F', 'Feminino'),
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    pele = RadioField(
        'Pele',
        choices=[
            ('Branca', 'Branca'),
            ('Parda', 'Parda'),
            ('Amarela', 'Amarela'),
            ('Preta', 'Preta'),
            ('indigena', 'indígena'),
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    local_nasc = RadioField(
        'Local de nascimento',
        choices=[
            ('Urbano', 'Urbano'),
            ('Rural', 'Rural'),
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    cidade = StringField(
        'Cidade',
        validators=[InputRequired('Preencha este campo')]
    )

    estado = StringField(
        'Estado',
        validators=[InputRequired('Preencha este campo')]
    )

    pais = StringField(
        'País',
        validators=[InputRequired('Preencha este campo')]
    )

    local_resid = RadioField(
        'Local de residência',
        choices=[
            ('Rural', 'Rural'),
            ('Urbano', 'Urbano'),
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    tempo_resid = IntegerField(
        'Há quantos anos reside neste local?',
        validators=[InputRequired('Preencha este campo')]
    )

    estado_civil = RadioField(
        'Qual o seu estado civil?',
        choices=[
            ('Solteiro', 'Solteiro(a)'),
            ('Casado', 'Casado(a)'),
            ('Divorciado', 'Divorciado'),
            ('Viuvo', 'Viúvo(a)'),
            ('Outro', 'Outro'),
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    escolaridade = RadioField(
        'Escolaridade',
        choices=[
            ('Fundamental', 'Fundamental'),
            ('Medio', 'Médio'),
            ('Graduacao', 'Graduação'),
            ('Pos_graduacao', 'Pós-graduação'),
            ('Mestrado', 'Mestrado'),
            ('Doutorado', 'Doutorado'),
        ],
        validators=[InputRequired('Preencha este campo')]
    )

    aposentadoria = RadioField(
        'Você é aposentado?',
        choices=[
            ('Nao', 'Não'),
            ('Tempo_servico', 'Por tempo de serviço'),
            ('Invalidez', 'Por invalidez'),
            ('Idade', 'Por idade'),
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    valor_apos = IntegerField(
        'Qual o valor, em reais (não contar centavos) da sua aposentadoria?',
        validators=[Optional()]
    )

    # MORADIA
    casa = RadioField(
        'Sua casa é',
        choices=[
            ('Propria', 'Própria'),
            ('Alugada', 'Alugada'),
            ('Cedida', 'Cedida/emprestada'),
            ('Outros', 'Outros'),
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    esgoto = RadioField(
        'O esgoto é',
        choices=[
            ('Publica', 'Rede pública'),
            ('septica', 'Fossa séptica'),
            ('Ceu_aberto', 'Céu aberto'),
            ('Outros', 'Outros'),
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    luz = RadioField(
        'Tem luz elétrica?',
        choices=[
            ('Sim', 'Sim'),
            ('Não', 'Não'),
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    lixo = RadioField(
        'O lixo é',
        choices=[
            ('Caminhao_lixo', 'Coletado pelo caminhão'),
            ('Queimado', 'Queimado'),
            ('Jogado', 'Jogado'),
            ('Enterrado', 'Enterrado'),
            ('Outros', 'Outros'),
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    meios_transporte = SelectMultipleField(
        'Quais os meios de transporte que você mais utiliza?',
        choices=[
            ('automovel', 'Automóvel'),
            ('Onibus', 'Ônibus'),
            ('Carroca', 'Carroça'),
            ('Bicicleta', 'Bicicleta'),
            ('A_pe', 'A pé'),
            ('Cavalo', 'A cavalo'),
            ('Caminhao', 'Caminhão'),
            ('Outros', 'Outros'),
        ],
        validators=[InputRequired('Selecione uma ou mais opções')],
        option_widget=widgets.CheckboxInput(), 
        widget=widgets.ListWidget(prefix_label=False)
    )

    # COMPOSIÇÃO FAMILIAR
    modo_vida = RadioField(
        'Atualmente, você vive sozinho ou acompanhado?',
        choices=[
            ('Sozinho', 'Sozinho'),
            ('conjuge', 'Moro com meu cônjuge'),
            ('Filhos', 'Moro com meus filhos'),
            ('Outros', 'Outros'),
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    satisf_vida = RadioField(
        'Você está satisfeito com a sua moradia atualmente?',
        choices=[
            ('Sim', 'Sim'),
            ('Nao', 'Não'),
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    # CONDIÇÕES DE SAÚDE E HÁBITOS DE VIDA 
    saude_geral = RadioField(
        'Em geral, você diria que sua saúde é: ',
        choices=[
            ('Otima', 'Ótima'),
            ('Boa', 'Boa'),
            ('Regular', 'Regular'),
            ('Ruim', 'Ruim'),
            ('Pessima', 'Péssima'),
        ],
        validators=[InputRequired('Selecione uma opção')]
    )

    Medicamentos = StringField(
        'Você toma algum medicamento? Se sim, anote os medicamentos utilizados abaixo',
        validators=[Optional()]
    )

    motivo_uso = RadioField(
        'Por que está tomando estes medicamentos?',
        choices=[
            ('Receita', 'Médico receitou'),
            ('Sugestao', 'Sugestão de conhecido'),
            ('TV', 'Rádio ou TV'),
            ('automedicacao', 'Conta própria'),
            ('Farmacia', 'Farmácia'),
            ('Benzedeira', 'Benzedeira ou curandor'),
        ],
        validators=[Optional()]
    )

    aquisicao = RadioField(
        'Como adquiriu estes medicamentos?',
        choices=[
            ('Comprou', 'Comprou'),
            ('SUS', 'SUS'),
            ('Seguro_saúde', 'Seguro de saúde'),
            ('Ganhou', 'Ganhou'),
            ('Outros', 'Outros'),
        ],
        validators=[Optional()]
    )

    # PROBLEMAS DE SAUDE

    reumatismo = RadioField('Reumatismo', choices=opcoes_resposta, validators=[InputRequired('Selecione uma opção')])
    asma_bronquite = RadioField('Asma ou bronquite', choices=opcoes_resposta, validators=[InputRequired('Selecione uma opção')])
    pressao_alta = RadioField('Pressão alta', choices=opcoes_resposta, validators=[InputRequired('Selecione uma opção')])
    varizes = RadioField('Varizes', choices=opcoes_resposta, validators=[InputRequired('Selecione uma opção')])
    diabetes = RadioField('Diabetes', choices=opcoes_resposta, validators=[InputRequired('Selecione uma opção')])
    obesidade = RadioField('Obesidade', choices=opcoes_resposta, validators=[InputRequired('Selecione uma opção')])
    derrame = RadioField('Derrame', choices=opcoes_resposta, validators=[InputRequired('Selecione uma opção')])
    incontinencia = RadioField('Incontinência urinária', choices=opcoes_resposta, validators=[InputRequired('Selecione uma opção')])
    prisao_ventre = RadioField('Prisão de ventre', choices=opcoes_resposta, validators=[InputRequired('Selecione uma opção')])
    insonia = RadioField('Insônia', choices=opcoes_resposta, validators=[InputRequired('Selecione uma opção')])
    catarata = RadioField('Catarata', choices=opcoes_resposta, validators=[InputRequired('Selecione uma opção')])
    problema_coluna = RadioField('Problemas de coluna', choices=opcoes_resposta, validators=[InputRequired('Selecione uma opção')])
    artrite_artrose = RadioField('Artrite ou artrose', choices=opcoes_resposta, validators=[InputRequired('Selecione uma opção')])
    osteoporose = RadioField('Osteoporose', choices=opcoes_resposta, validators=[InputRequired('Selecione uma opção')])
    nervos = RadioField('Problemas com nervos', choices=opcoes_resposta, validators=[InputRequired('Selecione uma opção')])
    tuberculose = RadioField('Tuberculose', choices=opcoes_resposta, validators=[InputRequired('Selecione uma opção')])
    cardiaco = RadioField('Problemas cardíacos', choices=opcoes_resposta, validators=[InputRequired('Selecione uma opção')])
    anemia = RadioField('Anemia', choices=opcoes_resposta, validators=[InputRequired('Selecione uma opção')])
    parkinson = RadioField('Parkinson', choices=opcoes_resposta, validators=[InputRequired('Selecione uma opção')])
    constipacao = RadioField('Incontinência fecal ou constipação', choices=opcoes_resposta, validators=[InputRequired('Selecione uma opção')])
    cancer = RadioField('Câncer', choices=opcoes_resposta, validators=[InputRequired('Selecione uma opção')])
    alzheimer = RadioField('Alzheimer', choices=opcoes_resposta, validators=[InputRequired('Selecione uma opção')])
    depressao = RadioField('Depressão', choices=opcoes_resposta, validators=[InputRequired('Selecione uma opção')])
    osteomioarticulares = RadioField('Dores osteomioarticulares', choices=opcoes_resposta, validators=[InputRequired('Selecione uma opção')])
    tontura = RadioField('Tontura', choices=opcoes_resposta, validators=[InputRequired('Selecione uma opção')])
    colesterol = RadioField('Colesterol', choices=opcoes_resposta, validators=[InputRequired('Selecione uma opção')])

    # ACESSO SERVIÇOS DE SAÚDE E APOIO FAMILIAR
    cuidador = SelectMultipleField(
        'Você tem alguem que lhe cuide quando está doente?',
        choices=[
            ('conjuge', 'Cônjuge'),
            ('Filho', 'Filho(a)'),
            ('familiar', 'Outro familiar'),
            ('amigo', 'Amigo ou vizinho'),
            ('Profissional', 'Profissional contratado'),
            ('Agente_saude', 'Agente comunitário de saúde'),
            ('Ninguem', 'Ninguém'),
            ('Outros', 'Outros'),
        ],
        validators=[InputRequired('Selecione uma ou mais opções')],
        option_widget=widgets.CheckboxInput(), 
        widget=widgets.ListWidget(prefix_label=False)
    )

    sexo_cuidador = RadioField(
        'Em caso afirmativo, qual é o sexo dessa pessoa?',
        choices=[
            ('M', 'Masculino'),
            ('F', 'Feminino'),
            ('Nao_tem', 'Não Tenho cuidador'),
        ],
        validators=[InputRequired('Selecione uma opção')],
    )

    idade_cuidador = RadioField(
        'A pessoa que cuida de você, é maior de 60 anos?',
        choices=[
            ('Maior_60', 'Sim'),
            ('Menor_60', 'Não'),
            ('NS', 'Não sei'),
            ('Nao_tem', 'Não Tenho cuidador'),
        ],
        validators=[InputRequired('Selecione uma opção')],
    )

    servico_saude = SelectMultipleField(
        'Durante o último ano, onde você foi quando se sentiu doente ou precisou de consultas médicas?',
        choices=[
            ('Nao_consultou', 'Não consultou, mesmo precisando'),
            ('Nao_precisou', 'Não ficou doente nem precisou de nenhuma consulta'),
            ('particular', 'Consultório particular'),
            ('hospital_particular', 'Serviço de emergência em hospital particular'),
            ('Samu', 'Samu/bombeiros'),
            ('Benzedeira', 'Benzedeira'),
            ('UBS', 'Unidade básica de saúde'),
            ('emergencia_municipal', 'Serviço de emergência municipal'),
            ('Farmacia', 'Farmácia'),
            ('Pronto_socorro', 'Pronto socorro'),
            ('Outro', 'Outro'),
        ],
        validators=[InputRequired('Selecione uma ou mais opções')],
        option_widget=widgets.CheckboxInput(), 
        widget=widgets.ListWidget(prefix_label=False)
    )

    submit = SubmitField('Salvar')