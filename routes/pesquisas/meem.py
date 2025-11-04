import os
from flask import Blueprint, render_template, redirect, session, url_for, flash, request
from supabase import create_client
from datetime import datetime

from FlaskWTF.pesquisas.meem_form import FormularioMeem
from ..pesquisador import limpar_sessao_pesquisa, acesso_pesq, validar_acesso_pesquisa
from ..adm import acesso_admin, validar_acesso_adm


meem_bp = Blueprint('meem', __name__)


supabase =  create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


# ==================== CALCULAR PONTUAÇÃO =====================
# def calcular_pontuacao(form):
#     total = sum(field.data for field in form if isinstance(field.data, int))
#     classificacao = "Demência" if total <= 24 else "Normal"
#     return total, classificacao


# ==================== CALCULAR PONTUAÇÃO =====================
def calcular_pontuacao(form, id_entrevistado):
    total = sum(field.data for field in form if isinstance(field.data, int))
    
    # OBTER ESCOLARIDADE (sempre existe devido à validação)
    id_vida_saude = supabase.table('estudos_geral')\
        .select('id')\
        .eq('id_entrevistado', id_entrevistado)\
        .eq('tipo', 'Vida e Saúde')\
        .execute().data[0]['id']
    
    escolaridade = supabase.table('info_pessoais')\
        .select('escolaridade')\
        .eq('id_estudos_geral', id_vida_saude)\
        .execute().data[0]['escolaridade']
    
    # CALCULAR CLASSIFICAÇÃO
    ponto_corte = 17 if escolaridade == 'Fundamental' else 24
    classificacao = "Demência" if total <= ponto_corte else "Normal"
    
    return total, classificacao

# ================== ROTA COLETA DADOS MEEM ===================
@meem_bp.route('/coleta_dados_meem/<int:id_entrevistado>', methods=['GET', 'POST'])
def coleta_dados_meem(id_entrevistado):

    token_url = request.args.get('token')
    token_sessao = session.get('token_pesquisa')

    if not token_url or token_url != token_sessao:
        return redirect(url_for('pesq.pg_pesq'))
    
    form = FormularioMeem()

    if form.validate_on_submit():
        user_id = session.get('id_usuario')

        estudos_geral_data = {
            'id_entrevistado': id_entrevistado, 
            'id_usuario': user_id, 
            'data_horario': datetime.now().isoformat(),
            'tipo': 'MEEM'
        }

        response_estudo = supabase.table('estudos_geral').insert(estudos_geral_data).execute()

        _id = response_estudo.data[0]['id']

        perguntas_data = {
            'id_estudos_geral': _id,
            'dia': form.dia.data,
            'mes': form.mes.data,
            'ano': form.ano.data,
            'semana': form.semana.data,
            'hora': form.hora.data,
            'local': form.local.data,
            'local_amplo': form.local_amplo.data,
            'bairro': form.bairro.data,
            'cidade': form.cidade.data,
            'estado': form.estado.data,
            'palavras': form.palavras.data,
            'calculo': form.calculo.data,
            'memoria': form.memoria.data,
            'objetos': form.objetos.data,
            'repeticao': form.repeticao.data,
            'comando_verbal': form.comando_verbal.data,
            'comando_escrito': form.comando_escrito.data,
            'escrita': form.escrita.data,
            'desenho': form.desenho.data
        }

        pontuacao, classificacao = calcular_pontuacao(form, id_entrevistado)
        perguntas_data['pontuacao'] = pontuacao
        perguntas_data['classificacao'] = classificacao

        supabase.table('perguntas_meem').insert(perguntas_data).execute()

        limpar_sessao_pesquisa()

        flash('Formulário registrado com sucesso!', 'info')
        return redirect(url_for('pesq.nova_pesquisa'))
    
    return render_template('pesquisas/meem.html', form=form, id_entrevistado=id_entrevistado)


# ================== ROTA VISUALIZAR MEEM ===================
@meem_bp.route("/visualizar_meem/<int:id>")
@acesso_pesq
@validar_acesso_pesquisa
def visualizar_meem(pesquisa):

    resposta_form = (
        supabase.table("perguntas_meem")
        .select("*")
        .eq("id_estudos_geral", pesquisa['id'])
        .maybe_single()
        .execute()
    )

    respostas = resposta_form.data if resposta_form else None
    if not respostas:
        return redirect(url_for("pesq.minhas_pesquisas"))
    
    pontuacao = respostas.get('pontuacao')
    classificacao = respostas.get('classificacao')

    dados_form = {
        **respostas
    }

    form = FormularioMeem(data=dados_form)
    for field in form:
        field.render_kw = {"disabled": True}

    return render_template(
        "pesquisas/meem.html",
        form=form,
        id_entrevistado=pesquisa["id_entrevistado"],
        visualizar=True,
        pontuacao=pontuacao,
        classificacao=classificacao
    )


# ================== ROTA EDITAR MEEM ===================
@meem_bp.route("/editar_meem/<int:id>", methods=['GET', 'POST'])
@acesso_pesq
@validar_acesso_pesquisa
def editar_meem(pesquisa):

    resposta_form = (
        supabase.table("perguntas_meem")
        .select("*")
        .eq("id_estudos_geral", pesquisa['id'])
        .maybe_single()
        .execute()
    )

    respostas = resposta_form.data
    if not respostas:
        return redirect(url_for("pesq.minhas_pesquisas"))

    form = FormularioMeem()

    if form.validate_on_submit():

        pontuacao, classificacao = calcular_pontuacao(form, pesquisa["id_entrevistado"])
         
        perguntas_data = {
            'dia': form.dia.data,
            'mes': form.mes.data,
            'ano': form.ano.data,
            'semana': form.semana.data,
            'hora': form.hora.data,
            'local': form.local.data,
            'local_amplo': form.local_amplo.data,
            'bairro': form.bairro.data,
            'cidade': form.cidade.data,
            'estado': form.estado.data,
            'palavras': form.palavras.data,
            'calculo': form.calculo.data,
            'memoria': form.memoria.data,
            'objetos': form.objetos.data,
            'repeticao': form.repeticao.data,
            'comando_verbal': form.comando_verbal.data,
            'comando_escrito': form.comando_escrito.data,
            'escrita': form.escrita.data,
            'desenho': form.desenho.data,
            'pontuacao': pontuacao,
            'classificacao': classificacao,  
        }
        
        houve_alteracao = any(respostas.get(campo) != perguntas_data[campo] for campo in perguntas_data)

        if houve_alteracao:
            supabase.table("perguntas_meem").update(perguntas_data).eq("id_estudos_geral", pesquisa['id']).execute()
            flash('Pesquisa atualizada com sucesso!', 'info')
        else:
            flash('Nenhuma alteração foi realizada.', 'secondary')

        return redirect(url_for('pesq.minhas_pesquisas'))

    if request.method == 'GET':
        form.dia.data = respostas.get("dia")
        form.mes.data = respostas.get("mes")
        form.ano.data = respostas.get("ano")
        form.semana.data = respostas.get("semana")
        form.hora.data = respostas.get("hora")
        form.local.data = respostas.get("local")
        form.local_amplo.data = respostas.get("local_amplo")
        form.bairro.data = respostas.get("bairro")
        form.cidade.data = respostas.get("cidade")
        form.estado.data = respostas.get("estado")
        form.palavras.data = respostas.get("palavras")
        form.calculo.data = respostas.get("calculo")
        form.memoria.data = respostas.get("memoria")
        form.objetos.data = respostas.get("objetos")
        form.repeticao.data = respostas.get("repeticao")
        form.comando_verbal.data = respostas.get("comando_verbal")
        form.comando_escrito.data = respostas.get("comando_escrito")
        form.escrita.data = respostas.get("escrita")
        form.desenho.data = respostas.get("desenho")
    
    return render_template(
        "pesquisas/meem.html",
        form=form,
        id_entrevistado=pesquisa["id_entrevistado"],
        editar=True,
        id_pesquisa=pesquisa['id']
    )


# ================== ROTA VISUALIZAR MEEM ADM ===================
@meem_bp.route("/visualizar_meem_admin/<int:id>")
@acesso_admin
@validar_acesso_adm
def visualizar_meem_admin(pesquisa):

    resposta_form = (
        supabase.table("perguntas_meem")
        .select("*")
        .eq("id_estudos_geral", pesquisa['id'])
        .maybe_single()
        .execute()
    )

    respostas = resposta_form.data if resposta_form else None

    if not respostas:
        return redirect(url_for("admin.visualizar_pesquisas"))
    
    pontuacao = respostas.get('pontuacao')
    classificacao = respostas.get('classificacao')

    dados_form = {
        **respostas
    }

    form = FormularioMeem(data=dados_form)
    for field in form:
        field.render_kw = {"disabled": True}

    return render_template(
        "pesquisas/meem.html",
        form=form,
        id_entrevistado=pesquisa["id_entrevistado"],
        visualizar=True,
        pontuacao=pontuacao,
        classificacao=classificacao,
        admin=True
    )
