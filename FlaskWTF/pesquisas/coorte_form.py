from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField
from wtforms.validators import InputRequired


class FormularioCoorte(FlaskForm):

    # SINAIS VITAIS
    pa = StringField(validators = [InputRequired('Informe a pressão arterial')])
    fc = IntegerField(validators = [InputRequired('Informe a frequência cardíaca')])
    saturacao = FloatField(validators = [InputRequired('Informe a saturação')])

    # TESTES MOTORES
    timed_up_go_1 = FloatField(validators = [InputRequired('Informe um valor')])
    timed_up_go_2 = FloatField(validators = [InputRequired('Informe um valor')])
    timed_up_go_3 = FloatField(validators = [InputRequired('Informe um valor')])
    
    chair_test = IntegerField(validators=[InputRequired('Informe as repetições')])
   
    pren_man_dir_1 = FloatField(validators = [InputRequired('Informe um valor')])
    pren_man_dir_2 = FloatField(validators = [InputRequired('Informe um valor')])
    pren_man_dir_3 = FloatField(validators = [InputRequired('Informe um valor')])
   

    pren_man_esq_1 = FloatField(validators = [InputRequired('Informe um valor')])
    pren_man_esq_2 = FloatField(validators = [InputRequired('Informe um valor')])
    pren_man_esq_3 = FloatField(validators = [InputRequired('Informe um valor')])

    # ANTROPOMETRIA
    massa = FloatField(validators = [InputRequired('Informe a massa corporal')])

    estatura = FloatField(validators = [InputRequired('Informe a estatura')])

    esp_polegar = FloatField(validators = [InputRequired('Informe a espessura')])

    quadril = FloatField(validators = [InputRequired('Informe a medida')])

    abdomen = FloatField(validators = [InputRequired('Informe a medida')])

    antebraco_dir = FloatField(validators = [InputRequired('Informe a medida')])
    antebraco_esq = FloatField(validators = [InputRequired('Informe a medida')])

    braco_rel_dir = FloatField(validators = [InputRequired('Informe a medida')])
    braco_rel_esq = FloatField(validators = [InputRequired('Informe a medida')])

    braco_ctr_dir = FloatField(validators = [InputRequired('Informe a medida')])
    braco_ctr_esq = FloatField(validators = [InputRequired('Informe a medida')])

    panturrilha_dir = FloatField(validators = [InputRequired('Informe a medida')])
    panturrilha_esq = FloatField(validators = [InputRequired('Informe a medida')])

    coxa_sup_dir = FloatField(validators = [InputRequired('Informe a medida')])
    coxa_sup_esq = FloatField(validators = [InputRequired('Informe a medida')])


    submit = SubmitField('Salvar')