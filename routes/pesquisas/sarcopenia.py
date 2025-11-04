import os
from flask import Blueprint, render_template, redirect, session, url_for, flash, request
from supabase import create_client
from datetime import datetime

from FlaskWTF.pesquisas.sarcopenia import FormularioSarcopenia
from ..pesquisador import limpar_sessao_pesquisa, validar_acesso_pesquisa, acesso_pesq
from ..adm import acesso_admin, validar_acesso_adm


sarcopenia_bp = Blueprint('sarcopenia', __name__)


supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


# =============================================================================
# FUNÇÃO AUXILIAR: CÁLCULO DE PONTUAÇÃO
# =============================================================================
def calcular_pontuacao(respostas):

    # Mapeamento das respostas para valores numéricos
    pontos = {
        'nenhuma':0, 
        'alguma':1, 
        'muita':2, 
        '1_a_3':1, 
        '4_ou_mais':2
    }

    # Lista dos campos que compõem a pontuação total
    campos = ['forca', 'apoio_marcha', 'levantar_cadeira', 'subir_escada', 'quedas']

    # Soma a pontuação de todos os campos
    pontuacao = sum(pontos.get(respostas.get(campo, ''), 0) for campo in campos)

    # Classificação baseada na pontuação total
    risco = "Alto risco de sarcopenia" if pontuacao >= 4 else "Baixo risco de sarcopenia"

    return pontuacao, risco


# =============================================================================
# ROTA: COLETA DE DADOS 
# =============================================================================
@sarcopenia_bp.route('/coleta_dados_sarcopenia/<int:id_entrevistado>', methods=['GET', 'POST'])
def coleta_dados_sarcopenia(id_entrevistado):

    token_url = request.args.get('token')
    token_sessao = session.get('token_pesquisa')

    # Se tokens não coincidem ou não existem, redireciona
    if not token_url or token_url != token_sessao:
        return redirect(url_for('pesq.pg_pesq'))
    
    # Inicializa o formulário de Sarcopenia
    form = FormularioSarcopenia()

    # Processa o formulário quando submetido
    if form.validate_on_submit():
        user_id = session.get('id_usuario')

        # Prepara dados para a tabela principal de estudos
        estudos_geral_data = {
            'id_entrevistado': id_entrevistado, 
            'id_usuario': user_id, 
            'data_horario': datetime.now().isoformat(),
            'tipo': 'Sarcopenia'
        }

        # Insere na tabela principal e obtém o ID gerado
        response_estudo = supabase.table('estudos_geral').insert(estudos_geral_data).execute()

        _id = response_estudo.data[0]['id']

        # Prepara os dados específicos do questionário Sarcopenia
        perguntas_data = {
            'id_estudos_geral': _id,
            'forca': form.forca.data,
            'apoio_marcha': form.apoio.data,
            'levantar_cadeira': form.levantar.data,
            'subir_escada': form.escada.data,
            'quedas': form.quedas.data,
        }

        # Calcula pontuação, classificação de risco e adiciona resultados ao dicionário perguntas_data
        pontuacao, risco = calcular_pontuacao(perguntas_data)
        perguntas_data['pontuacao_total'] = pontuacao
        perguntas_data['classificacao_risco'] = risco

        # Insere os dados específicos da Sarcopenia
        supabase.table('perguntas_sarcopenia').insert(perguntas_data).execute()

        limpar_sessao_pesquisa()

        flash('Formulário registrado com sucesso!', 'info')
        return redirect(url_for('pesq.nova_pesquisa'))
    
    # Renderiza o template para preenchimento do formulário
    return render_template('pesquisas/sarcopenia.html', form=form, id_entrevistado=id_entrevistado)


# =============================================================================
# ROTA: VISUALIZAR PESQUISA (MODO LEITURA)
# =============================================================================
@sarcopenia_bp.route("/visualizar_sarcopenia/<int:id>")
@acesso_pesq 
@validar_acesso_pesquisa 
def visualizar_sarcopenia(pesquisa):
   
    # Busca os dados específicos da pesquisa de Sarcopenia
    resposta_form = (
        supabase.table("perguntas_sarcopenia")
        .select("*")
        .eq("id_estudos_geral", pesquisa['id'])
        .maybe_single()
        .execute()
    )

    respostas = resposta_form.data if resposta_form else None

    if not respostas:
        return redirect(url_for("pesq.minhas_pesquisas"))
    
    pontuacao = respostas.get("pontuacao_total")
    risco = respostas.get("classificacao_risco")

    # Prepara dados para preencher o formulário
    dados_form = {
        "forca": respostas.get("forca"),
        "apoio": respostas.get("apoio_marcha"),
        "levantar": respostas.get("levantar_cadeira"),
        "escada": respostas.get("subir_escada"),
        "quedas": respostas.get("quedas"),
    }

    # Cria formulário com dados existentes
    form = FormularioSarcopenia(data=dados_form)
    for field in form:
        field.render_kw = {"disabled": True}

    # Renderiza template em modo visualização
    return render_template(
        "pesquisas/sarcopenia.html",
        form=form,
        id_entrevistado=pesquisa["id_entrevistado"],
        visualizar=True,
        pontuacao=pontuacao,
        risco=risco
    )


# =============================================================================
# ROTA: EDITAR PESQUISA EXISTENTE
# =============================================================================
@sarcopenia_bp.route("/editar_sarcopenia/<int:id>", methods=['GET', 'POST'])
@acesso_pesq
@validar_acesso_pesquisa
def editar_sarcopenia(pesquisa):
    
    # Busca dados atuais da pesquisa
    resposta_form = (
        supabase.table("perguntas_sarcopenia")
        .select("*")
        .eq("id_estudos_geral", pesquisa['id'])
        .maybe_single()
        .execute()
    )

    respostas = resposta_form.data

    form = FormularioSarcopenia()

    # Processa o formulário de edição
    if form.validate_on_submit():
        
        # Prepara novos dados do formulário
        dados_novos = {
            'forca': form.forca.data,
            'apoio_marcha': form.apoio.data,
            'levantar_cadeira': form.levantar.data,
            'subir_escada': form.escada.data,
            'quedas': form.quedas.data,
        }

        # Recalcula pontuação com os novos dados
        pontuacao, risco = calcular_pontuacao(dados_novos)
        dados_novos['pontuacao_total'] = pontuacao
        dados_novos['classificacao_risco'] = risco

        # Verifica se houve alterações
        houve_alteracao = any(respostas.get(campo) != dados_novos[campo] for campo in dados_novos)

        # Atualiza apenas se houver mudanças
        if houve_alteracao:
            supabase.table("perguntas_sarcopenia").update(dados_novos).eq("id_estudos_geral", pesquisa['id']).execute()
            flash('Pesquisa atualizada com sucesso!', 'info')
        else:
            flash('Nenhuma alteração foi realizada.', 'secondary')

        return redirect(url_for('pesq.minhas_pesquisas'))

    # Preenche o formulário com dados atuais (método GET)
    if request.method == 'GET':
        form.forca.data = respostas.get("forca")
        form.apoio.data = respostas.get("apoio_marcha")
        form.levantar.data = respostas.get("levantar_cadeira")
        form.escada.data = respostas.get("subir_escada")
        form.quedas.data = respostas.get("quedas")

    # Renderiza template em modo edição
    return render_template(
        "pesquisas/sarcopenia.html",
        form=form,
        id_entrevistado=pesquisa["id_entrevistado"],
        editar=True,
        id_pesquisa=pesquisa['id']
    )


# =============================================================================
# ROTA: VISUALIZAR PESQUISA (MODO ADMINISTRADOR)
# =============================================================================
@sarcopenia_bp.route("/visualizar_sarcopenia_admin/<int:id>")
@acesso_admin
@validar_acesso_adm
def visualizar_sarcopenia_admin(pesquisa):
  
    resposta_form = (
        supabase.table("perguntas_sarcopenia")
        .select("*")
        .eq("id_estudos_geral", pesquisa['id'])
        .maybe_single()
        .execute()
    )

    respostas = resposta_form.data if resposta_form else None

    if not respostas:
        return redirect(url_for("admin.visualizar_pesquisas"))
    
    pontuacao = respostas.get("pontuacao_total")
    risco = respostas.get("classificacao_risco")

    dados_form = {
        "forca": respostas.get("forca"),
        "apoio": respostas.get("apoio_marcha"),
        "levantar": respostas.get("levantar_cadeira"),
        "escada": respostas.get("subir_escada"),
        "quedas": respostas.get("quedas"),
    }

    form = FormularioSarcopenia(data=dados_form)
    for field in form:
        field.render_kw = {"disabled": True}

    return render_template(
        "pesquisas/sarcopenia.html",
        form=form,
        id_entrevistado=pesquisa["id_entrevistado"],
        visualizar=True,
        pontuacao=pontuacao,
        risco=risco,
        admin=True
    )