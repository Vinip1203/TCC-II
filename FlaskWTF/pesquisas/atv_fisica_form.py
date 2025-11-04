from flask_wtf import FlaskForm
from wtforms import IntegerField, TimeField, SubmitField
from wtforms.validators import InputRequired


class FormularioAtvFisica(FlaskForm):

    
    dias_caminhada = IntegerField(
        'Dias:',
        validators = [InputRequired('Informe o número de dias')]
    )

    duracao_caminhada = TimeField(
        'Tempo:',
        validators = [InputRequired('Informe a duração')]
    )

    atv_moderada = IntegerField(
        'Dias:',
        validators = [InputRequired('Informe o número de dias')]
    )

    temp_atv_moderada = TimeField(
        'Tempo:',
        validators = [InputRequired('Informe a duração')]
    )


    atv_vigorosa = IntegerField(
        'Dias:',
        validators = [InputRequired('Informe o número de dias')]
    )

    temp_atv_vigorosa = TimeField(
        'Tempo:',
        validators = [InputRequired('Informe a duração')]
    )


    temp_sentado_smn = TimeField(
        'Durante a semana:',
        validators = [InputRequired('Informe o tempo médio')]
    )

    temp_sentado_fds = TimeField(
        'No fim de semana:',
        validators = [InputRequired('Informe o tempo médio')]
    )

    submit = SubmitField('Salvar')