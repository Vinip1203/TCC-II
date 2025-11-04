import os
import secrets
from functools import wraps
from flask import Blueprint, render_template, redirect, session, url_for,flash, request
from supabase import create_client
from datetime import datetime, timedelta

from FlaskWTF.pesq_form import NovaPesquisaForm
from FlaskWTF.pesquisas.sarcopenia import FormularioSarcopenia


pesq_bp = Blueprint('pesq', __name__)


supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


# =============================================================================
# MAPEAMENTO DE TIPOS DE ESTUDO PARA BLUEPRINTS
# =============================================================================

# Dicionário que traduz nomes de estudos ("Coorte", "Atividade Física") para nomes técnicos das rotas ("coorte", "atv_fisica")
mapeamento_blueprints = {
    "Coorte": "coorte",
    "Atividade Física": "atv_fisica", 
    "Alimentação": "alimentacao",
    "Qualidade de Vida": "qual_vida",
    "Vida e Saúde": "vida_saude",
    "Sarcopenia": "sarcopenia",
    "Ansiedade": "ansiedade",
    "MEEM": "meem"
}


# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================

# Remove os dados de pesquisa da sessão do usuário. Usado quando uma pesquisa é cancelada ou finalizada.
def limpar_sessao_pesquisa():
    if 'token_pesquisa' in session:
        session.pop('token_pesquisa', None)
        session.pop('tipo_estudo', None)
        session.pop('id_entrevistado', None)


# Decorator verifica se o usuário está autenticado como pesquisador antes de acessar a rota
def acesso_pesq(f):
    @wraps(f) 
    def redirecionar(*args, **kwargs):
        if session.get('papel') != 'Pesquisador':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs) 
    return redirecionar


# Decorator para acessar uma pesquisa específica. Verifica se a pesquisa pertence ao usuário logado
def validar_acesso_pesquisa(f):
  
    @wraps(f)
    def wrapper(id, *args, **kwargs):
        user_id = session.get("id_usuario")
        
        resposta_pesquisa = (
            supabase.table("estudos_geral")
            .select("id, tipo, id_entrevistado")
            .eq("id", id)
            .eq("id_usuario", user_id)
            .maybe_single()
            .execute()
        )
        
        pesquisa = resposta_pesquisa.data if resposta_pesquisa else None
        
        if not pesquisa:
            return redirect(url_for("pesq.minhas_pesquisas"))

        return f(pesquisa, *args, **kwargs)
    return wrapper


# =============================================================================
# HOME
# =============================================================================
@pesq_bp.route('/pg_pesq')
@acesso_pesq 
def pg_pesq():
    return render_template('pesq/pg_pesq.html')


# =============================================================================
# INICIAR NOVA PESQUISA
# =============================================================================
@pesq_bp.route('/nova_pesquisa', methods=['GET', 'POST'])
@acesso_pesq
def nova_pesquisa():

    # Verifica se já existe uma pesquisa em andamento na sessão
    if 'token_pesquisa' in session:
        tipo_estudo = session.get('tipo_estudo')
        id_entrevistado = session.get('id_entrevistado')
        token_pesquisa = session.get('token_pesquisa')
        
        # Se há uma pesquisa em andamento, redireciona para continuá-la
        if tipo_estudo and id_entrevistado and token_pesquisa:
            endpoint_name = f'{tipo_estudo}.coleta_dados_{tipo_estudo}'
            flash('Você tem uma pesquisa em andamento. Conclua-a antes de iniciar uma nova.', 'warning')
            return redirect(url_for(endpoint_name, id_entrevistado=id_entrevistado, token=token_pesquisa))

    form = NovaPesquisaForm()

    if form.validate_on_submit():
        nome_entrevistado = form.nome_entrevistado.data.title()
        tipo_estudo = form.tipo_estudo.data

        # Verifica se o entrevistado já existe no banco
        existente = supabase.table('entrevistado').select('id').eq('nome_entrevistado', nome_entrevistado).execute()

        # Cria um novo registro ou retorna o ID do entrevistado existente
        if existente.data:
            id_entrevistado = existente.data[0]['id']
        else:
            novo_entrevistado = supabase.table('entrevistado').insert({'nome_entrevistado': nome_entrevistado}).execute()
            id_entrevistado = novo_entrevistado.data[0]['id']
            
        if tipo_estudo == 'meem':
            # Verifica se existe questionário "Vida e Saúde" para este entrevistado
            vida_saude_existente = supabase.table('estudos_geral').select('id').eq('id_entrevistado', id_entrevistado).eq('tipo', 'Vida e Saúde').execute()
            
            if not vida_saude_existente.data:
                flash('Para realizar o Mini-Exame de Estado Mental (MEEM), é necessário responder o questionário "Condições de Vida e Saúde das Populações Idosas".', 'warning')
                return render_template('pesq/nova_pesquisa.html', form=form)
        
        # Gera um token único para cada pesquisa
        token_pesquisa = secrets.token_urlsafe(16)

        # Armazena os dados na sessão
        session['token_pesquisa'] = token_pesquisa
        session['tipo_estudo'] = tipo_estudo
        session['id_entrevistado'] = id_entrevistado
        
        # Constrói o nome do endpoint dinamicamente e redireciona
        endpoint_name = f'{tipo_estudo}.coleta_dados_{tipo_estudo}'
        
        return redirect(url_for(endpoint_name, id_entrevistado=id_entrevistado, token=token_pesquisa))
    
    return render_template('pesq/nova_pesquisa.html', form=form)


# =============================================================================
# CANCELAR PESQUISA
# =============================================================================

# Cancela uma pesquisa em andamento e limpa os dados da sessão relacionados
@pesq_bp.route('/cancelar_pesquisa', methods=['POST'])
@acesso_pesq
def cancelar_pesquisa():
    limpar_sessao_pesquisa()
    flash('Pesquisa cancelada com sucesso', 'info')
    return redirect(url_for('pesq.nova_pesquisa'))


# =============================================================================
# LISTAR PRÉVIAS DE PESQUISAS REALIZADAS
# =============================================================================
@pesq_bp.route("/minhas_pesquisas")
@acesso_pesq
def minhas_pesquisas():
    id_usuario = session.get("id_usuario")

    # Obtém parâmetros de filtro da URL
    filtro_tipo = request.args.get("tipo")
    filtro_data = request.args.get("data")
    filtro_nome = request.args.get("nome")

    tipos_disponiveis = list(mapeamento_blueprints.keys())

    # Monta a busca básica pelos estudos no banco de dados
    query = (
        supabase.table("estudos_geral")
        .select("id, data_horario, tipo, entrevistado(nome_entrevistado)")
        .eq("id_usuario", id_usuario)
        .order("data_horario", desc=True)
    )

    # Aplica filtros conforme parâmetros
    if filtro_tipo:
        query = query.eq("tipo", filtro_tipo)

    if filtro_data:
        d = datetime.fromisoformat(filtro_data)
        query = query.gte("data_horario", d).lt("data_horario", d + timedelta(days=1))

    if filtro_nome:
        query = query.ilike("entrevistado.nome_entrevistado", f"%{filtro_nome}%")

    registros = query.execute().data or []

    estudos = [
        {
            "id": r["id"],
            "tipo": r["tipo"],
            "data": (ts := datetime.fromisoformat(r["data_horario"])).strftime("%d/%m/%Y"),
            "horario": ts.strftime("%H:%M"),
            "nome_entrevistado": r["entrevistado"]["nome_entrevistado"],
        }
        for r in registros
        if r.get("entrevistado") and r["entrevistado"].get("nome_entrevistado")
    ]

    return render_template(
        "pesq/minhas_pesquisas.html",
        estudos=estudos,
        filtro_tipo=filtro_tipo,
        filtro_data=filtro_data,
        filtro_nome=filtro_nome,
        tipos_disponiveis=tipos_disponiveis,
    )


# =============================================================================
# VISUALIZAR DADOS COLETADOS
# =============================================================================

# Visualiza uma pesquisa específica, redireciona para o blueprint apropriado baseado no tipo de estudo
@pesq_bp.route("/pesquisa/<int:id>")
@acesso_pesq
@validar_acesso_pesquisa
def visualizar_pesquisa(pesquisa):
    tipo = pesquisa["tipo"]
    blueprint = mapeamento_blueprints.get(tipo)
    return redirect(url_for(f'{blueprint}.visualizar_{blueprint}', id=pesquisa['id']))


# =============================================================================
# EDITAR 
# =============================================================================
@pesq_bp.route("/editar_pesquisa/<int:id>")
@acesso_pesq
@validar_acesso_pesquisa
def editar_pesquisa(pesquisa):
    tipo = pesquisa["tipo"]
    blueprint = mapeamento_blueprints.get(tipo)
    return redirect(url_for(f'{blueprint}.editar_{blueprint}', id=pesquisa['id']))