import os
import io
import zipfile
import csv
from functools import wraps
from flask import Blueprint, render_template, redirect, session, flash, url_for, request, send_file, Response
from werkzeug.security import generate_password_hash
from supabase import create_client
from email_validator import validate_email, EmailNotValidError
from datetime import datetime, timedelta

from FlaskWTF.adm_form import CadastroForm

admin_bp = Blueprint('admin', __name__)

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


# =============================================================================
# MAPEAMENTOS E CONFIGURAÇÕES
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

# Define quais tabelas do banco pertencem a cada tipo de estudo
tabelas = {
    "Coorte": ["sinais_vitais", "testes_motores", "antropometria"],
    "Atividade Física": ["perguntas_atv_fisica"],
    "Alimentação": ["perguntas_alimentacao"],
    "Qualidade de Vida": ["qld_vida_emocional", "qld_vida_fisica", "qld_vida_geral", "qld_vida_limitacao"],
    "Vida e Saúde": ["info_pessoais", "moradia", "composicao_familiar", "condicao_saude", "problemas_saude", "apoio_familiar_social"],
    "Sarcopenia": ["perguntas_sarcopenia"],
    "Ansiedade": ["perguntas_ansiedade"],
    "MEEM": ["perguntas_meem"]
}


# =============================================================================
# DECORADORES DE CONTROLE DE ACESSO
# =============================================================================

# Verifica se o usuário logado tem papel de administrador
def acesso_admin(f):
    @wraps(f) 
    def redirecionar(*args, **kwargs):
        if session.get('papel') != 'Administrador':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs) 
    return redirecionar


# Decorador para validar acesso a uma pesquisa específica
def validar_acesso_adm(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Obtém o id da pesquisa da URL
        id_pesquisa = kwargs.get('id')

        if not id_pesquisa:
            flash('ID da pesquisa não fornecido.', 'danger')
            return redirect(url_for('admin.todas_pesquisas'))
        
        # Busca a pesquisa no banco de dados pelo ID
        resposta_pesquisa = (
            supabase.table("estudos_geral")
            .select("*")
            .eq("id", id_pesquisa)
            .maybe_single()
            .execute()
        )
        
        pesquisa = resposta_pesquisa.data if resposta_pesquisa else None
        
        # Verifica se a pesquisa existe
        if not pesquisa:
            flash('Pesquisa não encontrada.', 'danger')
            return redirect(url_for("admin.todas_pesquisas"))

        # Passa o objeto 'pesquisa' completo para a função
        kwargs.pop('id', None)
        return f(pesquisa, *args, **kwargs)
    return wrapper


# =============================================================================
# HOME
# =============================================================================
@admin_bp.route('/pg_adm')
@acesso_admin 
def pg_adm():
    return render_template('adm/pg_adm.html')


# =============================================================================
# CADASTRO DE USUÁRIOS
# =============================================================================
@admin_bp.route('/cadastro', methods=['GET', 'POST'])
@acesso_admin 
def cadastrar_usuario():

    form = CadastroForm()

    if form.validate_on_submit():
        nome_usuario = form.nome_usuario.data.title()
        email = form.email.data.lower()
        senha = form.senha.data
        papel = form.papel.data

        # Validação de e-mail
        try:
            validate_email(email, check_deliverability=True)
        except EmailNotValidError:
            flash('Endereço de e-mail inválido.', 'danger')
            return render_template('adm/cadastro.html', form=form)
        
        # Verifica se já existe usuário com mesmo e-mail ou nome
        existente = supabase.table('usuarios').select('email, nome_usuario').or_(f"email.eq.{email},nome_usuario.eq.{nome_usuario}").execute()
        
        if existente.data:
            flash('Já existe um usuário com este e-mail ou nome de usuário.', 'danger')
            return render_template('adm/cadastro.html', form=form)
        
        # Gera hash da senha
        senha_hashed = generate_password_hash(senha)

        # Insere novo usuário no banco
        response = supabase.table('usuarios').insert({
            'nome_usuario': nome_usuario,
            'email': email,
            'senha': senha_hashed,
            'papel': papel
        }).execute()

        if response.data:
            flash('Usuário cadastrado com sucesso!', 'info')
            return redirect(url_for('admin.cadastrar_usuario'))
        else:
            flash('Erro ao cadastrar usuário.', 'danger')
            return redirect(url_for('admin.cadastrar_usuario'))
    
    return render_template('adm/cadastro.html', form=form)


# =============================================================================
# LISTAR PRÉVIAS DE PESQUISAS DISPONÍVEIS
# =============================================================================
@admin_bp.route("/visualizar_pesquisas")
@acesso_admin
def visualizar_pesquisas():

    # Obtém parâmetros de filtro da URL
    filtro_tipo = request.args.get("tipo")
    filtro_data = request.args.get("data")
    filtro_nome = request.args.get("nome")
    filtro_pesquisador = request.args.get("nome_pesquisador")

    # Lista de tipos de estudo disponíveis
    tipos_disponiveis = list(mapeamento_blueprints.keys())

    # Monta a busca básica pelos estudos no banco de dados
    query = (
        supabase.table("estudos_geral")
        .select("id, data_horario, tipo, entrevistado(nome_entrevistado), usuarios(nome_usuario)")
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

    if filtro_pesquisador:
        query = query.ilike("usuarios.nome_usuario", f"%{filtro_pesquisador}%")

    # Executa a query e obtém resultados
    registros = query.execute().data or []

    # Formata os dados para exibição
    estudos = [
        {
            "id": r["id"],
            "tipo": r["tipo"],
            "data": (ts := datetime.fromisoformat(r["data_horario"])).strftime("%d/%m/%Y"),
            "horario": ts.strftime("%H:%M"),
            "nome_entrevistado": r["entrevistado"]["nome_entrevistado"],
            "nome_pesquisador": r["usuarios"]["nome_usuario"] 
        }
        for r in registros
        if r.get("entrevistado") and r["entrevistado"].get("nome_entrevistado") and r.get("usuarios") and r["usuarios"].get("nome_usuario")
    ]

    return render_template(
        "adm/visualizar_pesquisas.html",
        estudos=estudos,
        filtro_tipo=filtro_tipo,
        filtro_data=filtro_data,
        filtro_nome=filtro_nome,
        filtro_pesquisador=filtro_pesquisador,
        tipos_disponiveis=tipos_disponiveis,
    )


# =============================================================================
# VISUALIZAR PESQUISA ESPECÍFICA
# =============================================================================
@admin_bp.route("/pesquisa_admin/<int:id>")
@acesso_admin
@validar_acesso_adm
def visualizar_pesquisa_admin(pesquisa):

    tipo = pesquisa["tipo"]
    blueprint = mapeamento_blueprints.get(tipo)
    
    # Redireciona para a rota específica do tipo de estudo
    if blueprint:
        return redirect(url_for(f'{blueprint}.visualizar_{blueprint}_admin', id=pesquisa['id']))
    else:
        return redirect(url_for("admin.todas_pesquisas"))
    

# =============================================================================
# EXCLUIR PESQUISA
# =============================================================================
@admin_bp.route("/excluir_pesquisa_admin/<int:id>", methods=['POST'])
@acesso_admin
def excluir_pesquisa_admin(id):
   
    resposta_pesquisa = (
        supabase.table("estudos_geral")
        .select("tipo")
        .eq("id", id)
        .maybe_single()
        .execute()
    )
    
    pesquisa = resposta_pesquisa.data
    
    # Exclui dados de todas as tabelas relacionadas
    for tabela in tabelas.get(pesquisa['tipo'], []):
        supabase.table(tabela).delete().eq("id_estudos_geral", id).execute()

    # Exclui o registro principal
    supabase.table("estudos_geral").delete().eq("id", id).execute()
    
    flash('Pesquisa excluída com sucesso!', 'info')
    return redirect(url_for('admin.visualizar_pesquisas'))


# =============================================================================
# EXPORTAR DADOS 
# =============================================================================
@admin_bp.route("/exportar", methods=['POST'])
@acesso_admin
def exportar():

    # Obtém os tipos de estudo selecionados no formulário de exportação
    tipos = request.form.getlist('tipos_estudo')
    
    def buscar_dados(tipo):
        # Busca os registros do tipo especificado, trazendo o ID e o nome do entrevistado.
        estudos = (
            supabase.table("estudos_geral")
            .select("id, entrevistado(nome_entrevistado)")
            .eq("tipo", tipo)
            .execute()
            .data
        )

        # Inicializa a lista que armazenará os dados de cada entrevistado (cada item representará uma linha do CSV).
        dados = []


        # Percorre todos os estudos retornados do banco e cria um dicionário base com o nome do entrevistado.
        # Este dicionário será gradualmente preenchido com os dados das diferentes tabelas relacionadas.
    
        for estudo in estudos:
            registro = {"nome_entrevistado": estudo["entrevistado"]["nome_entrevistado"]}

            for tabela in tabelas[tipo]:
                resultado = (
                    supabase.table(tabela)
                    .select("*")
                    .eq("id_estudos_geral", estudo["id"])
                    .execute()
                    .data
                )
                if resultado:
                    # Atualiza o dicionário 'registro' com os campos retornados.
                    # Remove campos técnicos ('id' e 'id_estudos_geral')
                    registro.update({
                        k: v for k, v in resultado[0].items()
                        if k not in {"id", "id_estudos_geral"}
                    })

            """
            Após percorrer todas as tabelas, o dicionário 'registro'
            conterá todas as informações de um determinado entrevistado.
            
            Exemplo:
                {
                    "nome_entrevistado": "Maria Souza",
                    "massa": 68.5,
                    "estatura": 1.70,
                    "imc": 23.7,
                    "pressao": "120/80"
                }
            
            Este registro é adicionado à lista final 'dados'.
            """
            dados.append(registro)
       
        return dados

    # Retorna uma string vazio se não há dados para exportar
    def gerar_csv(dados):
        if not dados:
            return "" 
        
        # Cria um buffer de texto em memória para armazenar o conteúdo do CSV.
        output = io.StringIO()

        writer = csv.DictWriter(output, fieldnames=dados[0].keys(), quoting=csv.QUOTE_ALL)
        writer.writeheader()

        # Percorre cada registro (entrevistado) e escreve uma linha no CSV
        for item in dados:
            writer.writerow({
                k: str(v).replace('\n', ' ').replace('\r', '') for k, v in item.items()
            })
        
        """
        Retorna o conteúdo final do CSV com o prefixo BOM (Byte Order Mark).
        O BOM é necessário para que o Excel reconheça corretamente o arquivo como UTF-8,
        evitando caracteres corrompidos (acentos, cedilhas etc.)
        """
        return "\ufeff" + output.getvalue()

    # Exportação única (apenas um tipo de estudo selecionado)
    if len(tipos) == 1:
        tipo = tipos[0]
        csv_data = gerar_csv(buscar_dados(tipo))
        
        mimetype = 'text/csv'

        # Retorna o arquivo CSV diretamente para download
        return Response(
            csv_data,
            mimetype=mimetype,
            headers={'Content-Disposition': f'attachment; filename="{tipo}.csv"'}
        )
    
    # Vários tipos selecionados: Compacta em um arquivo ZIP
    zip_buf = io.BytesIO() # Buffer de memória que armazenará o conteúdo do ZIP

    with zipfile.ZipFile(zip_buf, "w") as z:
        for tipo in tipos:
            csv_data = gerar_csv(buscar_dados(tipo))
            # Codifica o texto CSV em bytes (UTF-8 com BOM já incluso no conteúdo)
            encoded_data = csv_data.encode('utf-8')
            z.writestr(f"{tipo}.csv", encoded_data)
 
    # Retorna o ZIP para download
    zip_buf.seek(0)
    return send_file(zip_buf, as_attachment=True, download_name="dados_exportados.zip")