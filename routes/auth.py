import smtplib 
import os 
from datetime import datetime, timedelta
from uuid import uuid4
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import render_template, request, session, flash, url_for, redirect, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
from supabase import create_client

from FlaskWTF.auth_form import LoginForm, EsqueceuForm, RedefinirForm


# =============================================================================
# CONFIGURAÇÕES
# =============================================================================

# Blueprint para rotas de autenticação
auth_bp = Blueprint('auth', __name__)

# Conexão com Supabase (banco de dados)
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# Dicionário para controle de tempo no envio de e-mails
# Estrutura: { "email@exemplo.com": datetime_do_ultimo_envio }
emails_em_espera = {}


# =============================================================================
# FUNÇÃO AUXILIAR: ENVIO DE E-MAIL
# =============================================================================
def enviar_email(destinatario, assunto, mensagem):
   
   # Configurações do servidor de e-mail (variáveis de ambiente)
    smtp_server = os.getenv("EMAIL_SMTP")
    smtp_port = int(os.getenv("EMAIL_PORTA"))
    remetente = os.getenv("EMAIL_REMETENTE")
    senha = os.getenv("EMAIL_SENHA")

    # Cria mensagem MIME para suportar conteúdo HTML
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto
    msg.attach(MIMEText(mensagem, 'html'))

    try:
        # Envia e-mail via SMTP
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(remetente, senha)
            server.sendmail(remetente, destinatario, msg.as_string())
    except Exception as e:
        raise # Propaga erro para tratamento na rota


# =============================================================================
# ROTA: LOGIN DE USUÁRIOS
# =============================================================================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    # Se já logado, redireciona para página conforme papel
    if session.get('logged_in'):
        return redirect(url_for('admin.pg_adm') if session ['papel'] == 'Administrador' else url_for('pesq.pg_pesq'))
    
    #Inicializa formulário de login
    form = LoginForm()

    # Processamento do formulário submetido (POST)
    if form.validate_on_submit():
        email = form.email.data
        senha = form.senha.data
        remember_me = form.remember_me.data

        # Consulta banco de dados: Busca usuário pelo e-mail
        response = supabase.table('usuarios').select('id', 'senha', 'papel').eq('email', email).execute()

        # Verifica se o usuário existe
        if response.data:
            usuario = response.data[0]

            # Verifica senha (compara hash)
            if check_password_hash(usuario['senha'], senha):
                # Cria sessão do usuário
                session['logged_in'] = True
                session['papel'] = usuario['papel']
                session['id_usuario'] = usuario['id']
                session.permanent = remember_me

                return redirect(url_for('admin.pg_adm') if session['papel'] == 'Administrador' else url_for('pesq.pg_pesq'))

        # Credenciais inválidas (exibe mensagem de erro)
        flash('Credenciais inválidas.', 'danger')

    # Renderiza o template
    return render_template('auth/login.html', form=form)


# =============================================================================
# ROTA: SOLICITAÇÃO DE RECUPERAÇÃO DE SENHA
# =============================================================================
@auth_bp.route('/esqueci_senha', methods=['GET', 'POST'])
def esqueci_senha():
    form = EsqueceuForm()

    if form.validate_on_submit():
        email = form.email.data

        # Verifica se e-mail existe no banco de dados
        response = supabase.table('usuarios').select('email').eq('email', email).execute()

        if not response.data:
            flash('E-mail não encontrado.', 'danger')
            return redirect(url_for('auth.esqueci_senha'))

        # Verifica solicitações recentes
        if email in emails_em_espera:
            ultimo_envio = emails_em_espera[email]
            proximo_envio = ultimo_envio + timedelta(minutes=2)

            if datetime.now() < proximo_envio:
                flash('Por favor, aguarde para uma nova solicitação', 'warning')
                return redirect(url_for('auth.esqueci_senha'))
        
        # Remove tokens anteriores do mesmo e-mail
        supabase.table('tokens_recuperacao').delete().eq('email', email).execute()
        
        # Gera token único
        token = str(uuid4())
        expira_em = (datetime.now() + timedelta(minutes=15)).isoformat() # Expira em 15min
        
        supabase.table('tokens_recuperacao').insert({
            'email': email,
            'token': token,
            'expira_em': expira_em
        }).execute()

        # Prepara e envia e-mail com link
        link = url_for('auth.recuperar_senha', token=token, _external=True)
        assunto = "Redefinição de Senha"
        mensagem = render_template('auth/email.html', link=link)
       
        try:
            enviar_email(email, assunto, mensagem)
            emails_em_espera[email] = datetime.now()
            flash('E-mail enviado! Verifique sua caixa de entrada (ou spam).', 'info')
        except Exception as e:
            flash(f'Erro ao enviar e-mail: {str(e)}. Tente novamente mais tarde.', 'danger')

        return redirect(url_for('auth.esqueci_senha'))

    return render_template('auth/esqueci_senha.html', form=form)


# =============================================================================
# ROTA: REDEFINIÇÃO DE SENHA
# =============================================================================
@auth_bp.route('/recuperar_senha', methods=['GET', 'POST'])
def recuperar_senha():

    # Recupera token via parâmetro na URL: /recuperar_senha?token=abc123...
    token = request.args.get('token') 
    form = RedefinirForm()

    response = supabase.table('tokens_recuperacao').select('*').eq('token', token).execute()

    # Verifica se token existe no banco de dados
    if not response.data:
        flash('Token inválido ou expirado.', 'danger')
        return redirect(url_for('auth.login'))

    # Extrai dados do token válido
    dados = response.data[0]
    email = dados['email']
    expira_em = datetime.fromisoformat(dados['expira_em'])

    # Remove token expirado e redireciona
    if datetime.now() > expira_em:
        supabase.table('tokens_recuperacao').delete().eq('token', token).execute()
        flash('Token expirado. Por favor, solicite uma nova redefinição de senha.', 'danger')
        return redirect(url_for('auth.login'))

    # Processa formulário de nova senha
    if form.validate_on_submit():
        nova_senha = form.nova_senha.data

        # Gera hash e atualiza a nova senha
        senha_hash = generate_password_hash(nova_senha)

        supabase.table('usuarios').update({'senha': senha_hash}).eq('email', email).execute()
        supabase.table('tokens_recuperacao').delete().eq('token', token).execute()

        flash('Senha redefinida! Faça login com a nova senha.', 'info')
        return redirect(url_for('auth.login'))

    return render_template('auth/redefinir_senha.html', form=form, token=token)


# =============================================================================
# ROTA: LOGOUT DO SISTEMA
# =============================================================================
@auth_bp.route('/logout')
def logout():
    # Remove todos os dados da sessão
    session.clear() 
    flash('Sua sessão foi encerrada', 'info')
    return redirect(url_for('auth.login'))