import os
from flask import render_template, session, flash, url_for, redirect, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
from supabase import create_client
from email_validator import validate_email, EmailNotValidError

from FlaskWTF.perfil_form import PerfilForm


perfil_bp = Blueprint('perfil', __name__)


supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


# =============================================================================
# ROTA: EXIBIR E ATUALIZAR PERFIL DO USUÁRIO
# =============================================================================
@perfil_bp.route('/perfil', methods=['GET', 'POST'])
def exibir_atualizar_perfil():

    # Obtém o ID do usuário da sessão atual
    user_id = session.get('id_usuario')

    if not user_id:
        return redirect(url_for('auth.login'))
    
    # Busca os dados atuais do usuário no banco de dados
    response = supabase.table('usuarios').select('nome_usuario, email, senha').eq('id', user_id).execute()
    usuario = response.data[0]

    form = PerfilForm()

    if form.validate_on_submit():
        # Dicionário para armazenar os campos que serão atualizados
        updates = {}

        novo_email = form.novo_email.data
        senha_atual = form.senha_atual.data
        nova_senha = form.nova_senha.data
        confirmar_senha = form.confirmar_senha.data

        # Verifica se o usuário alterou o email
        if novo_email and novo_email != usuario['email']:
            try:
                # Valida o formato do email e verifica se o domínio existe
                validate_email(novo_email, check_deliverability=True)
            except EmailNotValidError:
                flash('Endereço de e-mail inválido.', 'danger')
                return render_template('perfil.html', form=form, usuario=usuario)
            
            # Verifica se o novo email já está em uso por outro usuário
            existente = supabase.table('usuarios').select('id').eq('email', novo_email).neq('id', user_id).execute()

            if existente.data:
                flash('Este novo e-mail já está em uso por outro usuário.', 'danger')
                return render_template('perfil.html', form=form, usuario=usuario)

            updates['email'] = novo_email

        # Verifica se o usuário preencheu algum campo de senha
        if senha_atual or nova_senha or confirmar_senha:

            if not all([senha_atual, nova_senha, confirmar_senha]):
                flash('Para alterar a senha, todos os campos de senha devem ser preenchidos.', 'warning')
                return render_template('perfil.html', form=form, usuario=usuario)

            # Verifica se a senha atual fornecida confere com a senha armazenada
            if not check_password_hash(usuario['senha'], senha_atual):
                flash('A senha atual está incorreta.', 'danger')
                return render_template('perfil.html', form=form, usuario=usuario)

            # Verifica se a nova senha e a confirmação são iguais
            if nova_senha != confirmar_senha:
                flash('A nova senha e a confirmação não coincidem.', 'danger')
                return render_template('perfil.html', form=form, usuario=usuario)

            updates['senha'] = generate_password_hash(nova_senha)
        
        # Se há atualizações para fazer, executa no banco de dados
        if updates:
            supabase.table('usuarios').update(updates).eq('id', user_id).execute()
            flash('Perfil atualizado com sucesso!', 'info')

            response = supabase.table('usuarios').select('nome_usuario, email, senha').eq('id', user_id).execute()
            if response.data:
                usuario = response.data[0]
            
            # Retorna o template com formulário limpo e dados atualizados
            return render_template('perfil.html', form=PerfilForm(), usuario=usuario)
        else:
            flash('Nenhuma alteração foi realizada.', 'warning')

    return render_template('perfil.html', form=form, usuario=usuario)