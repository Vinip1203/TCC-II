import os
from flask import Blueprint, render_template, redirect, session, url_for, flash, request
from supabase import create_client
from datetime import datetime

from FlaskWTF.pesquisas.alimentacao_form import FormularioAlimentacao
from ..pesquisador import limpar_sessao_pesquisa, acesso_pesq, validar_acesso_pesquisa
from ..adm import acesso_admin, validar_acesso_adm


alimentacao_bp = Blueprint('alimentacao', __name__)


supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


# =============================================================================
# ROTA: COLETA DE DADOS DA PESQUISA (NOVA PESQUISA)
# =============================================================================
@alimentacao_bp.route('/coleta_dados_alimentacao/<int:id_entrevistado>', methods=['GET', 'POST'])
def coleta_dados_alimentacao(id_entrevistado):
    
    # O token é passado via URL e comparado com o token armazenado na sessão
    token_url = request.args.get('token')
    token_sessao = session.get('token_pesquisa')

    # Se tokens não coincidem ou não existem, redireciona
    if not token_url or token_url != token_sessao:
        return redirect(url_for('pesq.pg_pesq'))

    # Inicializa o formulário
    form = FormularioAlimentacao()

    # Processa o formulário quando submetido e valida os campos preenchidos
    if form.validate_on_submit():
        user_id = session.get('id_usuario')
        
        # Prepara dados para a tabela principal de estudos
        estudos_geral_data = {
            'id_entrevistado': id_entrevistado, 
            'id_usuario': user_id, 
            'data_horario': datetime.now().isoformat(),
            'tipo': 'Alimentação'
        }

        # Insere na tabela principal e obtém o ID gerado
        response_estudo = supabase.table('estudos_geral').insert(estudos_geral_data).execute()
        _id = response_estudo.data[0]['id']

        """
        FORM.DATA: Contém TODOS os dados do formulário preenchido pelo usuário

        Quando o usuário submete o formulário, o Flask-WTF automaticamente:

        1. Pega os dados do request.form (dados HTTP POST do navegador)
        2. Valida cada campo conforme as regras do FormularioAlimentacao  
        3. Armazena os valores validados em form.data
        
        form.data retorna um dicionário como:

        {
            'frutas_frequencia': 'diariamente',
            'verduras_frequencia': 'semanalmente',
            'carnes_frequencia': 'raramente',
            'csrf_token': 'abc123...',
            'submit': 'Enviar'
        }

        """

        # Prepara os dados específicos para a tabela de perguntas_alimentacao
        perguntas_data = {
            'id_estudos_geral': _id,
            **form.data # O operador ** desempacota todas as chaves e valores do dicionário
        }
        
        campos_remover = ['csrf_token', 'submit']

        for campo in campos_remover:
            perguntas_data.pop(campo, None)
        
        # Insere os dados específicos na tabela de Alimentação
        supabase.table('perguntas_alimentacao').insert(perguntas_data).execute()
        
        # Limpa a sessão de pesquisa (permite iniciar nova pesquisa)
        limpar_sessao_pesquisa()

        flash('Formulário registrado com sucesso!', 'info')
        return redirect(url_for('pesq.nova_pesquisa'))

    # Renderiza o template para preenchimento do formulário (método GET)
    # Ou re-renderiza se houver erros de validação (método POST com erros)
    return render_template('pesquisas/alimentacao.html', form=form, id_entrevistado=id_entrevistado)


# =============================================================================
# ROTA: VISUALIZAR PESQUISA (MODO LEITURA)
# =============================================================================
@alimentacao_bp.route("/visualizar_alimentacao/<int:id>")
@acesso_pesq
@validar_acesso_pesquisa
def visualizar_alimentacao(pesquisa):

    # Busca os dados específicos da pesquisa de Alimentação
    resposta_form = (
        supabase.table("perguntas_alimentacao")
        .select("*")
        .eq("id_estudos_geral", pesquisa['id']) # Filtra pelo ID da pesquisa
        .maybe_single()
        .execute()
    )

    # Extrai os dados da resposta, se existirem
    respostas = resposta_form.data if resposta_form else None

    # Se não encontrou a pesquisa no banco, redireciona para lista de pesquisas
    if not respostas:
        return redirect(url_for("pesq.minhas_pesquisas"))
    
    # OPERADOR **: Desempacota o dicionário 'respostas' para preencher o formulário
    dados_form = {**respostas}

    # Cria o formulário já preenchido com os dados do banco
    form = FormularioAlimentacao(data=dados_form)

    # Desabilita todos os campos (modo leitura)
    for field in form:
        field.render_kw = {"disabled": True}

    # Renderiza template em modo visualização
    return render_template(
        "pesquisas/alimentacao.html",
        form=form,
        id_entrevistado=pesquisa["id_entrevistado"],
        visualizar=True
    )


# =============================================================================
# ROTA: EDITAR PESQUISA EXISTENTE
# =============================================================================
@alimentacao_bp.route("/editar_alimentacao/<int:id>", methods=['GET', 'POST'])
@acesso_pesq
@validar_acesso_pesquisa
def editar_alimentacao(pesquisa):

    # Busca dados atuais da pesquisa
    resposta_form = (
        supabase.table("perguntas_alimentacao")
        .select("*")
        .eq("id_estudos_geral", pesquisa['id'])
        .maybe_single()
        .execute()
    )

    respostas = resposta_form.data if resposta_form else None

    if not respostas:
        return redirect(url_for("pesq.minhas_pesquisas"))

    # Inicializa o formulário (vazio inicialmente)
    form = FormularioAlimentacao()

    # Processa o formulário quando usuário salva as alterações (POST)
    if form.validate_on_submit():

        """
        OPERADOR ** AQUI: Pega os dados ATUALIZADOS do formulário

        form.data contém os NOVOS valores que o usuário acabou de digitar
        
        Exemplo de form.data:

        {
           'frutas_frequencia': 'semanalmente',    # ← Usuário mudou de 'diariamente'
           'verduras_frequencia': 'diariamente',   # ← Usuário mudou de 'semanalmente'
           'carnes_frequencia': 'raramente',       # ← Manteve o mesmo
           'csrf_token': 'abc123...',
           'submit': 'Salvar'
        }
        
        """
        
        dados_novos = {**form.data}

        # Remove campos técnicos do Flask-WTF
        campos_remover = ['csrf_token', 'submit']
        
        for campo in campos_remover:
            dados_novos.pop(campo, None)
        
        # Compara dados novos com dados originais para ver se realmente houve mudanças
        houve_alteracao = any(respostas.get(campo) != dados_novos.get(campo) for campo in dados_novos if campo in respostas)

        if houve_alteracao:
            # Atualiza apenas se houver alterações
            supabase.table("perguntas_alimentacao").update(dados_novos).eq("id_estudos_geral", pesquisa['id']).execute()
            flash('Pesquisa atualizada com sucesso!', 'info')
        else:
            flash('Nenhuma alteração foi realizada.', 'secondary')

        return redirect(url_for('pesq.minhas_pesquisas'))

    # MÉTODO GET: Quando o usuário ABRE a página para editar
    if request.method == 'GET':
        # Preenche o formulário com os dados atuais do banco
        form = FormularioAlimentacao(data=respostas)
    
    # Renderiza o template em modo edição
    return render_template(
        "pesquisas/alimentacao.html",
        form=form,
        id_entrevistado=pesquisa["id_entrevistado"],
        editar=True,
        id_pesquisa=pesquisa['id']
    )


# =============================================================================
# ROTA: VISUALIZAR PESQUISA (MODO ADMINISTRADOR)
# =============================================================================
@alimentacao_bp.route("/visualizar_alimentacao_admin/<int:id>")
@acesso_admin
@validar_acesso_adm
def visualizar_alimentacao_admin(pesquisa):
   
    
    resposta_form = (
        supabase.table("perguntas_alimentacao")
        .select("*")
        .eq("id_estudos_geral", pesquisa['id'])
        .maybe_single()
        .execute()
    )

    respostas = resposta_form.data if resposta_form else None

    if not respostas:
        return redirect(url_for("admin.visualizar_pesquisas"))

    dados_form = {
        **respostas
    }

    form = FormularioAlimentacao(data=dados_form)
    for field in form:
        field.render_kw = {"disabled": True}

    return render_template(
        "pesquisas/alimentacao.html",
        form=form,
        id_entrevistado=pesquisa["id_entrevistado"],
        visualizar=True,
        admin=True
    )