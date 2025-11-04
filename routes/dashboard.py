import os
from flask import Blueprint, render_template
from markupsafe import Markup
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from supabase import create_client

# Importa decorator para acesso administrativo
from .adm import acesso_admin

# Inicializa o blueprint do dashboard
dashboard_bp = Blueprint('dashboard', __name__)

# Configuração do cliente Supabase
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


# =============================================================================
# ROTA PRINCIPAL: DASHBOARD
# =============================================================================
@dashboard_bp.route("/dashboard")
@acesso_admin
def dashboard():
    
    # Busca dados de todas as tabelas necessárias do Supabase
    dados = {
        'estudos': supabase.table("estudos_geral").select("id, id_entrevistado").execute().data or [],
        'info_pessoais': supabase.table("info_pessoais").select("id_estudos_geral, data_nasc, sexo, escolaridade, valor_apos").execute().data or [],
        'antropometria': supabase.table("antropometria").select("id_estudos_geral, massa, estatura").execute().data or [],
        'problemas_saude': supabase.table("problemas_saude").select("*").execute().data or [],
        'atividade_fisica': supabase.table("perguntas_atv_fisica").select("nivel_atividade").execute().data or []
    }
    
    # Gera todos os gráficos baseados nos dados coletados
    graficos = {
        'idade': gerar_grafico_idade(dados['info_pessoais']),
        'sexo': gerar_grafico_sexo(dados['info_pessoais']),
        'imc': gerar_grafico_imc(dados['antropometria']),
        'doencas': gerar_grafico_doencas(dados['problemas_saude']),
        'aposentadoria': gerar_grafico_aposentadoria(dados['info_pessoais']),
        'atividade': gerar_grafico_atividade(dados['atividade_fisica'])
    }
    
    # Calcula totais de entrevistados e pesquisas
    totais = calcular_totais(dados['estudos'])
    
    return render_template("adm/dashboard.html", graficos=graficos, totais=totais)


# =============================================================================
# FUNÇÃO AUXILIAR: CÁLCULO DE TOTAIS
# =============================================================================
def calcular_totais(estudos):
    
    if not estudos:
        return {'total_entrevistados': 0, 'total_pesquisas': 0}
    
    df = pd.DataFrame(estudos)
    return {
        'total_entrevistados': df['id_entrevistado'].nunique(),  # Conta valores únicos de entrevistados
        'total_pesquisas': len(df)  # Conta total de pesquisas
    }


# =============================================================================
# FUNÇÃO AUXILIAR: GRÁFICO VAZIO
# =============================================================================
def gerar_grafico_vazio(titulo):
    
    fig = go.Figure()
    
    fig.add_annotation(
        text="Sem dados disponíveis",
        # xref="paper",
        # yref="paper",
        # x=0.5,
        # y=0.5,
        showarrow=False,
        font=dict(size=16, color="gray")
    )
    
    fig.update_layout(
        title=titulo,
        height=400,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        
    )
    
    # Converte o gráfico em  HTML
    return Markup(fig.to_html(full_html=False, config={"displayModeBar": False}))


# =============================================================================
# GRÁFICO DISTRIBUIÇÃO POR IDADE
# =============================================================================
def gerar_grafico_idade(info_pessoais):

    if not info_pessoais:
        return gerar_grafico_vazio("Distribuição por Idade")
    
    df = pd.DataFrame(info_pessoais)
    df['data_nasc'] = pd.to_datetime(df['data_nasc'])

    # Calcula idade em anos a partir da data de nascimento
    df['idade'] = (pd.to_datetime('today') - df['data_nasc']).dt.days // 365
    df = df[df['idade'].between(0, 120)]  # Filtra idades válidas
    
    # Define intervalos de faixas etárias
    bins = [0, 30, 45, 60, 75, 90, 120]
    labels = ['<30', '30-44', '45-59', '60-74', '75-89', '90+']

    # Categoriza as idades nas faixas definidas
    df['faixa_etaria'] = pd.cut(df['idade'], bins=bins, labels=labels, right=False)
    
    # Conta quantas pessoas há em cada faixa etária
    contagem = df['faixa_etaria'].value_counts().sort_index()
    
    # Cria gráfico de barras usando Plotly Express
    fig = px.bar(
        x=contagem.index,
        y=contagem.values,
        title="Distribuição por Idade",
        labels={'x': 'Faixa Etária', 'y': 'Quantidade'}
    )
    
    return Markup(fig.to_html(full_html=False, config={"displayModeBar": False}))


# =============================================================================
# GRÁFICO DISTRIBUIÇÃO POR SEXO
# =============================================================================
def gerar_grafico_sexo(info_pessoais):
   
    if not info_pessoais:
        return gerar_grafico_vazio("Distribuição por Sexo")
    
    df = pd.DataFrame(info_pessoais)
    contagem = df['sexo'].value_counts()
    
    # Cria gráfico de pizza
    fig = px.pie(
        values=contagem.values,
        names=contagem.index,
        title="Distribuição por Sexo"
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    return Markup(fig.to_html(full_html=False, config={"displayModeBar": False}))


# =============================================================================
# GRÁFICO IMC (ÍNDICE DE MASSA CORPORAL)
# =============================================================================
def gerar_grafico_imc(antropometria):
  
    if not antropometria:
        return gerar_grafico_vazio("Distribuição por IMC")
    
    df = pd.DataFrame(antropometria)

    # Calcula IMC
    df['imc'] = df['massa'] / ((df['estatura'] / 100) ** 2)
    
    # Define categorias de IMC segundo classificação padrão
    bins = [0, 18.5, 25, 30, 35, 40, 100]
    labels = ['Abaixo peso', 'Normal', 'Sobrepeso', 'Obesidade I', 'Obesidade II', 'Obesidade III']
    df['categoria_imc'] = pd.cut(df['imc'], bins=bins, labels=labels, right=False)
    
    contagem = df['categoria_imc'].value_counts()
    
    fig = px.pie(
        values=contagem.values,
        names=contagem.index,
        title="Distribuição por IMC",
        hole=0.4 
    )
    
    fig.update_traces(textposition='inside', textinfo='percent')
    
    return Markup(fig.to_html(full_html=False, config={"displayModeBar": False}))


# =============================================================================
# GRÁFICO DOENÇAS MAIS COMUNS
# =============================================================================
def gerar_grafico_doencas(problemas_saude):
    if not problemas_saude:
        return gerar_grafico_vazio("Doenças Mais Comuns")
    
    df = pd.DataFrame(problemas_saude)
    
    # Filtra apenas colunas de doenças (ignora ids)
    colunas_doencas = [col for col in df.columns if col not in ['id', 'id_estudos_geral']]
    
    # Cria DataFrame com todas as contagens 
    contagens = pd.DataFrame({
        'doenca': colunas_doencas,
        'total': [df[col].isin(['Tem_nao_interfere', 'Tem_interfere']).sum() for col in colunas_doencas],
        'nao_interfere': [(df[col] == 'Tem_nao_interfere').sum() for col in colunas_doencas],
        'interfere': [(df[col] == 'Tem_interfere').sum() for col in colunas_doencas]
    })
    
    # Obtem as doenças que mais aparecem
    top_5 = contagens.nlargest(5, 'total')
    
    
    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Tem e não interfere', 
        x=top_5['doenca'].str.replace('_', ' ').str.title(), 
        y=top_5['nao_interfere']))
    
    fig.add_trace(go.Bar(
        name='Tem e interfere', 
        x=top_5['doenca'].str.replace('_', ' ').str.title(), 
        y=top_5['interfere']))
    
    fig.update_layout(
        title="Doenças Mais Comuns",
        xaxis_title="Doenças", 
        yaxis_title="Quantidade de Pessoas",
        barmode='stack' # Gráfico de barras empilhadas
    )
    
    return Markup(fig.to_html(full_html=False, config={"displayModeBar": False}))


# =============================================================================
# GRÁFICO APOSENTADORIA VS ESCOLARIDADE
# =============================================================================
def gerar_grafico_aposentadoria(info_pessoais):
   
    if not info_pessoais:
        return gerar_grafico_vazio("Aposentadoria vs Escolaridade")
    
    df = pd.DataFrame(info_pessoais)
    
    # Remove registros com dados faltantes e valores zero
    df = df.dropna(subset=['valor_apos', 'escolaridade', 'sexo'])
    df = df[df['valor_apos'] > 0]
    
    if df.empty:
        return gerar_grafico_vazio("Aposentadoria vs Escolaridade")
    
    # Agrupa dados por escolaridade e sexo, calculando média dos valores
    dados_agrupados = df.groupby(['escolaridade', 'sexo'])['valor_apos'].mean().reset_index()
    
    # Gráfico de barras agrupadas usando Plotly Express
    fig = px.bar(
        dados_agrupados,
        x='escolaridade',
        y='valor_apos',
        color='sexo',
        title="Aposentadoria vs Escolaridade",
        barmode='group',  # Barras agrupadas lado a lado
        labels={'valor_apos': 'Valor Médio da Aposentadoria', 'escolaridade': 'Escolaridade'}
    )
    
    return Markup(fig.to_html(full_html=False, config={"displayModeBar": False}))


# =============================================================================
# GRÁFICO NÍVEIS DE ATIVIDADE FÍSICA
# =============================================================================
def gerar_grafico_atividade(atividade_fisica):
    
    if not atividade_fisica:
        return gerar_grafico_vazio("Níveis de Atividade")
    
    df = pd.DataFrame(atividade_fisica)
    contagem = df['nivel_atividade'].value_counts()
    
    # Define ordem específica para os níveis de atividade
    ordem_niveis = ['Muito Ativo', 'Ativo', 'Irregularmente Ativo A', 'Irregularmente Ativo B', 'Sedentário']
    
    # Garante que todos os níveis apareçam, mesmo com contagem zero
    contagem_completa = {}
    for nivel in ordem_niveis:
        contagem_completa[nivel] = contagem.get(nivel, 0)
    
    # Cria gráfico de barras ordenado
    fig = px.bar(
        x=list(contagem_completa.keys()),
        y=list(contagem_completa.values()),
        title="Níveis de Atividade Física",
        labels={'x': 'Nível de Atividade', 'y': 'Quantidade de Pessoas'}
    )
    
    # Rotaciona labels do eixo X para melhor legibilidade
    fig.update_layout(xaxis_tickangle=-45)
    
    return Markup(fig.to_html(full_html=False, config={"displayModeBar": False}))