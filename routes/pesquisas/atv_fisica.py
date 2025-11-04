import os
import pandas as pd
from flask import Blueprint, render_template, redirect, session, url_for, flash, request
from supabase import create_client
from datetime import datetime
from FlaskWTF.pesquisas.atv_fisica_form import FormularioAtvFisica
from ..pesquisador import limpar_sessao_pesquisa, acesso_pesq, validar_acesso_pesquisa
from ..adm import acesso_admin, validar_acesso_adm


atv_fisica_bp = Blueprint('atv_fisica', __name__)


supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


# ================== CALCULAR NIVEL DE ATIVIDADE FISICA ===================
def nivel_atv(respostas):
    
    dias_cam = respostas['caminhada']
    tempo_cam = respostas['tc']
    dias_mod = respostas['atv_moderada']
    tempo_mod = respostas['t_atv_mod']
    dias_vig = respostas['atv_vigorosa']
    tempo_vig = respostas['t_atv_vig']
    
    def para_minutos(tempo_str):
        h, m, s = map(int, tempo_str.split(':'))
        return h * 60 + m
    
    min_cam = para_minutos(tempo_cam)
    min_mod = para_minutos(tempo_mod)
    min_vig = para_minutos(tempo_vig)
    
    total_min_semana = (dias_cam * min_cam) + (dias_mod * min_mod) + (dias_vig * min_vig)
    total_dias_semana = dias_cam + dias_mod + dias_vig
    
    if min_cam < 10 and min_mod < 10 and min_vig < 10:
        return "Sedentário"
    
    criterio_1a = (dias_vig >= 5 and min_vig >= 30)
   
    criterio_1b = (dias_vig >= 3 and min_vig >= 20) and \
                 ((dias_mod >= 5 and min_mod >= 30) or (dias_cam >= 5 and min_cam >= 30))
    
    if criterio_1a or criterio_1b:
        return "Muito Ativo"
    
    criterio_2a = (dias_vig >= 3 and min_vig >= 20) 
    criterio_2b = (dias_mod >= 5 and min_mod >= 30) or (dias_cam >= 5 and min_cam >= 30)  
    criterio_2c = (total_dias_semana >= 5 and total_min_semana >= 150) 
    
    if criterio_2a or criterio_2b or criterio_2c:
        return "Ativo"
    
    criterio_3a = (total_dias_semana >= 5) or (total_min_semana >= 150) 
    
    if criterio_3a:
        return "Irregularmente Ativo A"
    else:
        return "Irregularmente Ativo B"


# ================== ROTA COLETA DADOS ATIVIDADE FISICA ===================
@atv_fisica_bp.route('/coleta_dados_atv_fisica/<int:id_entrevistado>', methods=['GET', 'POST'])
def coleta_dados_atv_fisica(id_entrevistado):

    token_url = request.args.get('token')
    token_sessao = session.get('token_pesquisa')

    if not token_url or token_url != token_sessao:
        return redirect(url_for('pesq.pg_pesq'))
    
    form = FormularioAtvFisica()

    if form.validate_on_submit():
        user_id = session.get('id_usuario')

        estudos_geral_data = {
            'id_entrevistado': id_entrevistado, 
            'id_usuario': user_id, 
            'data_horario': datetime.now().isoformat(),
            'tipo': 'Atividade Física'
        }

        response_estudo = supabase.table('estudos_geral').insert(estudos_geral_data).execute()

        _id = response_estudo.data[0]['id']

        def time_to_str(t):
            return t.strftime('%H:%M:%S')

        perguntas_data = {
            'id_estudos_geral': _id,
            'caminhada': form.dias_caminhada.data,
            'tc': time_to_str(form.duracao_caminhada.data),
            'atv_moderada': form.atv_moderada.data,
            't_atv_mod': time_to_str(form.temp_atv_moderada.data),
            'atv_vigorosa': form.atv_vigorosa.data,
            't_atv_vig': time_to_str(form.temp_atv_vigorosa.data),
            'ts_semana': time_to_str(form.temp_sentado_smn.data),
            'ts_fim_sem': time_to_str(form.temp_sentado_fds.data),
        }

        nivel = nivel_atv(perguntas_data)

        perguntas_data['nivel_atividade'] = nivel

        supabase.table('perguntas_atv_fisica').insert(perguntas_data).execute()

        limpar_sessao_pesquisa()

        flash('Formulário registrado com sucesso!', 'info')
        return redirect(url_for('pesq.nova_pesquisa'))
    
    return render_template('pesquisas/atv_fisica.html', form=form, id_entrevistado=id_entrevistado)


# ================== ROTA VISUALIZAR ATIVIDADE FISICA ===================
@atv_fisica_bp.route("/visualizar_atv_fisica/<int:id>")
@acesso_pesq
@validar_acesso_pesquisa
def visualizar_atv_fisica(pesquisa):

    resposta_form = (
        supabase.table("perguntas_atv_fisica")
        .select("*")
        .eq("id_estudos_geral", pesquisa['id'])
        .maybe_single()
        .execute()
    )

    respostas = resposta_form.data if resposta_form else None

    if not respostas:
        return redirect(url_for("pesq.minhas_pesquisas"))
    
    nivel = respostas.get("nivel_atividade")
    
    def str_to_time(time_str):
        return datetime.strptime(time_str, '%H:%M:%S').time()
    
    dados_form = {
        "dias_caminhada": respostas.get("caminhada"),
        "duracao_caminhada": str_to_time(respostas.get("tc")),
        "atv_moderada": respostas.get("atv_moderada"),
        "temp_atv_moderada": str_to_time(respostas.get("t_atv_mod")),
        "atv_vigorosa": respostas.get("atv_vigorosa"),
        "temp_atv_vigorosa": str_to_time(respostas.get("t_atv_vig")),
        "temp_sentado_smn": str_to_time(respostas.get("ts_semana")),
        "temp_sentado_fds": str_to_time(respostas.get("ts_fim_sem")),
    }

    form = FormularioAtvFisica(data=dados_form)
    for field in form:
        field.render_kw = {"disabled": True}

    return render_template(
        "pesquisas/atv_fisica.html",
        form=form,
        id_entrevistado=pesquisa["id_entrevistado"],
        visualizar=True,
        nivel_atividade=nivel
    )


# ================== ROTA EDITAR ATIVIDADE FISICA ===================
@atv_fisica_bp.route("/editar_atv_fisica/<int:id>", methods=['GET', 'POST'])
@acesso_pesq
@validar_acesso_pesquisa
def editar_atv_fisica(pesquisa):

    resposta_form = (
        supabase.table("perguntas_atv_fisica")
        .select("*")
        .eq("id_estudos_geral", pesquisa['id'])
        .maybe_single()
        .execute()
    )

    respostas = resposta_form.data

    form = FormularioAtvFisica()

    if form.validate_on_submit():

        def time_to_str(t):
            return t.strftime('%H:%M:%S')
        
        dados_novos = {
            "caminhada": form.dias_caminhada.data,
            "tc": time_to_str(form.duracao_caminhada.data),
            "atv_moderada": form.atv_moderada.data,
            "t_atv_mod": time_to_str(form.temp_atv_moderada.data),
            "atv_vigorosa": form.atv_vigorosa.data,
            "t_atv_vig": time_to_str(form.temp_atv_vigorosa.data),
            "ts_semana": time_to_str(form.temp_sentado_smn.data),
            "ts_fim_sem": time_to_str(form.temp_sentado_fds.data),
        }

        nivel = nivel_atv(dados_novos)
        dados_novos['nivel_atividade'] = nivel

        houve_alteracao = any(respostas.get(campo) != dados_novos[campo] for campo in dados_novos)

        if houve_alteracao:
            supabase.table("perguntas_atv_fisica").update(dados_novos).eq("id_estudos_geral", pesquisa['id']).execute()
            flash('Pesquisa atualizada com sucesso!', 'info')
        else:
            flash('Nenhuma alteração foi realizada.', 'secondary')

        return redirect(url_for('pesq.minhas_pesquisas'))
    
    if request.method == 'GET':

        def str_to_time(time_str):
            return datetime.strptime(time_str, '%H:%M:%S').time()
        
        form.dias_caminhada.data = respostas.get("caminhada")
        form.duracao_caminhada.data = str_to_time(respostas.get("tc"))
        form.atv_moderada.data = respostas.get("atv_moderada")
        form.temp_atv_moderada.data = str_to_time(respostas.get("t_atv_mod"))
        form.atv_vigorosa.data = respostas.get("atv_vigorosa")
        form.temp_atv_vigorosa.data = str_to_time(respostas.get("t_atv_vig"))
        form.temp_sentado_smn.data = str_to_time(respostas.get("ts_semana"))
        form.temp_sentado_fds.data = str_to_time(respostas.get("ts_fim_sem"))
    
    return render_template(
        "pesquisas/atv_fisica.html",
        form=form,
        id_entrevistado=pesquisa["id_entrevistado"],
        editar=True,
        id_pesquisa=pesquisa['id']
    )


# ================== ROTA VISUALIZAR ATIVIDADE FISICA ADM ===================
@atv_fisica_bp.route("/visualizar_atv_fisica_admin/<int:id>")
@acesso_admin
@validar_acesso_adm
def visualizar_atv_fisica_admin(pesquisa):

    resposta_form = (
        supabase.table("perguntas_atv_fisica")
        .select("*")
        .eq("id_estudos_geral", pesquisa['id'])
        .maybe_single()
        .execute()
    )

    respostas = resposta_form.data if resposta_form else None

    if not respostas:
        return redirect(url_for("admin.visualizar_pesquisas"))
    
    def str_to_time(time_str):
        return datetime.strptime(time_str, '%H:%M:%S').time()
    
    dados_form = {
        "dias_caminhada": respostas.get("caminhada"),
        "duracao_caminhada": str_to_time(respostas.get("tc")),
        "atv_moderada": respostas.get("atv_moderada"),
        "temp_atv_moderada": str_to_time(respostas.get("t_atv_mod")),
        "atv_vigorosa": respostas.get("atv_vigorosa"),
        "temp_atv_vigorosa": str_to_time(respostas.get("t_atv_vig")),
        "temp_sentado_smn": str_to_time(respostas.get("ts_semana")),
        "temp_sentado_fds": str_to_time(respostas.get("ts_fim_sem")),
    }

    form = FormularioAtvFisica(data=dados_form)
    for field in form:
        field.render_kw = {"disabled": True}
    
    nivel = respostas.get("nivel_atividade")

    return render_template(
        "pesquisas/atv_fisica.html",
        form=form,
        id_entrevistado=pesquisa["id_entrevistado"],
        visualizar=True,
        admin=True,
        nivel_atividade=nivel,
    )