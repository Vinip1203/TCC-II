import os
from flask import Blueprint, render_template, redirect, session, url_for, flash, request
from supabase import create_client
from datetime import datetime

from FlaskWTF.pesquisas.ansiedade_form import FormularioAnsiedade
from ..pesquisador import limpar_sessao_pesquisa, acesso_pesq, validar_acesso_pesquisa
from ..adm import acesso_admin, validar_acesso_adm


ansiedade_bp = Blueprint('ansiedade', __name__)


supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


# ====================== CALCULAR PONTUAÇÃO ========================
def calcular_pontuacao(respostas):
    campos = [f"p{i}" for i in range(1, 21)]
    return sum(1 for campo in campos if respostas.get(campo) == 'concordo')


# ================== ROTA COLETA DADOS ANSIEDADE ===================
@ansiedade_bp.route('/coleta_dados_ansiedade/<int:id_entrevistado>', methods=['GET', 'POST'])
def coleta_dados_ansiedade(id_entrevistado):

    token_url = request.args.get('token')
    token_sessao = session.get('token_pesquisa')

    if not token_url or token_url != token_sessao:
        return redirect(url_for('pesq.pg_pesq'))

    form = FormularioAnsiedade()

    if form.validate_on_submit():
        user_id = session.get('id_usuario')

        estudos_geral_data = {
            'id_entrevistado': id_entrevistado, 
            'id_usuario': user_id, 
            'data_horario': datetime.now().isoformat(),
            'tipo': 'Ansiedade'
        }

        response_estudo = supabase.table('estudos_geral').insert(estudos_geral_data).execute()

        id_estudos_geral = response_estudo.data[0]['id']

        perguntas_data = {
            'id_estudos_geral': id_estudos_geral, 
            'p1': form.p1.data,
            'p2': form.p2.data,
            'p3': form.p3.data,
            'p4': form.p4.data,
            'p5': form.p5.data,
            'p6': form.p6.data,
            'p7': form.p7.data,
            'p8': form.p8.data,
            'p9': form.p9.data,
            'p10': form.p10.data,
            'p11': form.p11.data,
            'p12': form.p12.data,
            'p13': form.p13.data,
            'p14': form.p14.data,
            'p15': form.p15.data,
            'p16': form.p16.data,
            'p17': form.p17.data,
            'p18': form.p18.data,
            'p19': form.p19.data,
            'p20': form.p20.data,
        }

        perguntas_data['pontuacao_total'] = calcular_pontuacao(perguntas_data)

        supabase.table('perguntas_ansiedade').insert(perguntas_data).execute()
        
        limpar_sessao_pesquisa()

        flash('Formulário registrado com sucesso!', 'info')
        return redirect(url_for('pesq.nova_pesquisa'))
    
    return render_template('pesquisas/ansiedade.html', form=form, id_entrevistado=id_entrevistado)


# ================== ROTA VISUALIZAR ANSIEDADE ===================
@ansiedade_bp.route("/visualizar_ansiedade/<int:id>")
@acesso_pesq
@validar_acesso_pesquisa
def visualizar_ansiedade(pesquisa):

    resposta_form = (
        supabase.table("perguntas_ansiedade")
        .select("*")
        .eq("id_estudos_geral", pesquisa['id'])
        .maybe_single()
        .execute()
    )

    respostas = resposta_form.data if resposta_form else None
    if not respostas:
        return redirect(url_for("pesq.minhas_pesquisas"))

    pontuacao = calcular_pontuacao(respostas)

    dados_form = {
        **respostas
    }

    form = FormularioAnsiedade(data=dados_form)
    for field in form:
        field.render_kw = {"disabled": True}

    return render_template(
        "pesquisas/ansiedade.html",
        form=form,
        id_entrevistado=respostas["id_estudos_geral"],
        visualizar=True,
        pontuacao=pontuacao
    )


# ================== ROTA EDITAR ANSIEDADE ===================
@ansiedade_bp.route("/editar_ansiedade/<int:id>", methods=['GET', 'POST'])
@acesso_pesq
@validar_acesso_pesquisa
def editar_ansiedade(pesquisa):

    resposta_form = (
        supabase.table("perguntas_ansiedade")
        .select("*")
        .eq("id_estudos_geral", pesquisa['id'])
        .maybe_single()
        .execute()
    )

    respostas = resposta_form.data
    if not respostas:
        return redirect(url_for("pesq.minhas_pesquisas"))

    form = FormularioAnsiedade()

    if form.validate_on_submit():
        perguntas_data = {
            'p1': form.p1.data,
            'p2': form.p2.data,
            'p3': form.p3.data,
            'p4': form.p4.data,
            'p5': form.p5.data,
            'p6': form.p6.data,
            'p7': form.p7.data,
            'p8': form.p8.data,
            'p9': form.p9.data,
            'p10': form.p10.data,
            'p11': form.p11.data,
            'p12': form.p12.data,
            'p13': form.p13.data,
            'p14': form.p14.data,
            'p15': form.p15.data,
            'p16': form.p16.data,
            'p17': form.p17.data,
            'p18': form.p18.data,
            'p19': form.p19.data,
            'p20': form.p20.data,
        }

        perguntas_data['pontuacao_total'] = calcular_pontuacao(perguntas_data)

        houve_alteracao = any(respostas.get(campo) != perguntas_data[campo] for campo in perguntas_data)

        if houve_alteracao:
            supabase.table("perguntas_ansiedade").update(perguntas_data).eq("id_estudos_geral", pesquisa['id']).execute()
            flash('Pesquisa atualizada com sucesso!', 'info')
        else:
            flash('Nenhuma alteração foi realizada.', 'secondary')

        return redirect(url_for('pesq.minhas_pesquisas'))

    if request.method == 'GET':
        form.p1.data = respostas.get("p1")
        form.p2.data = respostas.get("p2")
        form.p3.data = respostas.get("p3")
        form.p4.data = respostas.get("p4")
        form.p5.data = respostas.get("p5")
        form.p6.data = respostas.get("p6")
        form.p7.data = respostas.get("p7")
        form.p8.data = respostas.get("p8")
        form.p9.data = respostas.get("p9")
        form.p10.data = respostas.get("p10")
        form.p11.data = respostas.get("p11")
        form.p12.data = respostas.get("p12")
        form.p13.data = respostas.get("p13")
        form.p14.data = respostas.get("p14")
        form.p15.data = respostas.get("p15")
        form.p16.data = respostas.get("p16")
        form.p17.data = respostas.get("p17")
        form.p18.data = respostas.get("p18")
        form.p19.data = respostas.get("p19")
        form.p20.data = respostas.get("p20")

    return render_template(
        "pesquisas/ansiedade.html",
        form=form,
        id_entrevistado=pesquisa["id_entrevistado"],
        editar=True,
        id_pesquisa=pesquisa['id']
    )


# ================== ROTA VISUALIZAR ANSIEDADE ADM ===================
@ansiedade_bp.route("/visualizar_ansiedade_admin/<int:id>")
@acesso_admin
@validar_acesso_adm
def visualizar_ansiedade_admin(pesquisa):

    resposta_form = (
        supabase.table("perguntas_ansiedade")
        .select("*")
        .eq("id_estudos_geral", pesquisa['id'])
        .maybe_single()
        .execute()
    )

    respostas = resposta_form.data if resposta_form else None

    if not respostas:
        return redirect(url_for("admin.visualizar_pesquisas"))

    pontuacao = calcular_pontuacao(respostas)

    dados_form = {
        **respostas
    }

    form = FormularioAnsiedade(data=dados_form)
    for field in form:
        field.render_kw = {"disabled": True}

    return render_template(
        "pesquisas/ansiedade.html",
        form=form,
        id_entrevistado=respostas["id_estudos_geral"],
        visualizar=True,
        pontuacao=pontuacao,
        admin=True
    )
