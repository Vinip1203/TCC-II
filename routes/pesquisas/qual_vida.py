import os
from flask import Blueprint, render_template, redirect, session, url_for, flash, request
from supabase import create_client
from datetime import datetime

from FlaskWTF.pesquisas.qual_vida_form import FormularioQualidadeVida
from ..pesquisador import limpar_sessao_pesquisa, acesso_pesq, validar_acesso_pesquisa
from ..adm import acesso_admin, validar_acesso_adm


qual_vida_bp = Blueprint ('qual_vida', __name__)


supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


# ================== ROTA COLETA DADOS QUALIDADE VIDA ===================
@qual_vida_bp.route('/coleta_dados_qual_vida/<int:id_entrevistado>', methods=['GET', 'POST'])
def coleta_dados_qual_vida(id_entrevistado):

    token_url = request.args.get('token')
    token_sessao = session.get('token_pesquisa')

    if not token_url or token_url != token_sessao:
        return redirect(url_for('pesq.pg_pesq'))

    form = FormularioQualidadeVida()

    if form.validate_on_submit():
        user_id = session.get('id_usuario')

        estudos_geral_data = {
            'id_entrevistado': id_entrevistado, 
            'id_usuario': user_id, 
            'data_horario': datetime.now().isoformat(),
            'tipo': 'Qualidade de Vida'
        }

        response_estudo = supabase.table('estudos_geral').insert(estudos_geral_data).execute()

        _id = response_estudo.data[0]['id']

        qld_vida_geral_data = {
            'id_estudos_geral': _id,
            'saude_geral': form.saude_geral.data,
            'idade': form.idade.data,
            'obediencia': form.obediencia.data,
            'saudavel': form.saudavel.data,
            'saude_pior': form.saude_pior.data,
            'avl_saude': form.avl_saude.data,
        }


        qld_vida_fisica_data = {
            'id_estudos_geral': _id,
            'atv_rigorosa': form.atv_rigorosa.data,
            'atv_moderada': form.atv_moderada.data,
            'carregar_mant': form.carregar_mant.data,
            'subir_lance': form.subir_lance.data,
            'subir_escada': form.subir_escada.data,
            'flexionar': form.flexionar.data,
            'andar_1km': form.andar_1km.data,
            'andar_quart': form.andar_quart.data,
            'andar_vq': form.andar_vq.data,
            'banho': form.banho.data,
            'dor_corpo': form.dor_corpo.data,
            'dor_afetou': form.dor_afetou.data,
        }

        
        qld_vida_emo_data = {
            'id_estudos_geral': _id,
            'vigor': form.vigor.data,
            'nervoso': form.nervoso.data,
            'deprimido': form.deprimido.data,
            'calmo': form.calmo.data,
            'energia': form.energia.data,
            'desanimado': form.desanimado.data,
            'esgotado': form.esgotado.data,
            'feliz': form.feliz.data,
            'cansado': form.cansado.data,
        }


        qld_vida_limitacao_data = {
            'id_estudos_geral': _id,
            'temp_atv_fis': form.temp_atv_fis.data,
            'qtd_atv_fis': form.qtd_atv_fis.data,
            'limitado_fis': form.limitado_fis.data,
            'dif_fis': form.dif_fis.data,
            'temp_atv_emo': form.temp_atv_emo.data,
            'qtd_atv_emo': form.qtd_atv_emo.data,
            'cuidado_atv': form.cuidado_atv.data,
            'social': form.social.data,
            'temp_social': form.temp_social.data,
        }

        supabase.table('qld_vida_geral').insert(qld_vida_geral_data).execute()
        supabase.table('qld_vida_fisica').insert(qld_vida_fisica_data).execute()
        supabase.table('qld_vida_emocional').insert(qld_vida_emo_data).execute()
        supabase.table('qld_vida_limitacao').insert(qld_vida_limitacao_data).execute()

        limpar_sessao_pesquisa()

        flash('Formulário registrado com sucesso!', 'info')
        return redirect(url_for('pesq.nova_pesquisa'))

    return render_template('pesquisas/qual_vida.html', form=form, id_entrevistado=id_entrevistado)




# ================== ROTA VISUALIZAR QUALIDADE VIDA ===================
@qual_vida_bp.route("/visualizar_qual_vida/<int:id>")
@acesso_pesq
@validar_acesso_pesquisa
def visualizar_qual_vida(pesquisa):

    resposta_form = (
        supabase.table("qld_vida_completo")
        .select("*")
        .eq("id", pesquisa['id'])
        .maybe_single()
        .execute()
    )

    respostas = resposta_form.data if resposta_form else None

    if not respostas:
        return redirect(url_for("pesq.minhas_pesquisas"))
    
    dados_form = {
        **respostas
    }

    form = FormularioQualidadeVida(data=dados_form)
    for field in form:
        field.render_kw = {"disabled": True}

    return render_template(
        "pesquisas/qual_vida.html",
        form=form,
        id_entrevistado=pesquisa["id_entrevistado"],
        visualizar=True
    )


# ================== ROTA EDITAR QUALIDADE VIDA ===================
@qual_vida_bp.route("/editar_qual_vida/<int:id>", methods=['GET', 'POST'])
@acesso_pesq
@validar_acesso_pesquisa
def editar_qual_vida(pesquisa):

    resposta_form = (
        supabase.table("qld_vida_completo")
        .select("*")
        .eq("id", pesquisa['id'])
        .maybe_single()
        .execute()
    )

    respostas = resposta_form.data if resposta_form else None

    if not respostas:
        return redirect(url_for("pesq.minhas_pesquisas"))
    
    form = FormularioQualidadeVida()

    if form.validate_on_submit():
        
        dados_tabelas = {

            "qld_vida_geral": {
                "saude_geral": form.saude_geral.data,
                "idade": form.idade.data,
                "obediencia": form.obediencia.data,
                "saudavel": form.saudavel.data,
                "saude_pior": form.saude_pior.data,
                "avl_saude": form.avl_saude.data,
            },

            "qld_vida_fisica": {
                "atv_rigorosa": form.atv_rigorosa.data,
                "atv_moderada": form.atv_moderada.data,
                "carregar_mant": form.carregar_mant.data,
                "subir_lance": form.subir_lance.data,
                "subir_escada": form.subir_escada.data,
                "flexionar": form.flexionar.data,
                "andar_1km": form.andar_1km.data,
                "andar_quart": form.andar_quart.data,
                "andar_vq": form.andar_vq.data,
                "banho": form.banho.data,
                "dor_corpo": form.dor_corpo.data,
                "dor_afetou": form.dor_afetou.data,
            },

            "qld_vida_emocional": {
                "vigor": form.vigor.data,
                "nervoso": form.nervoso.data,
                "deprimido": form.deprimido.data,
                "calmo": form.calmo.data,
                "energia": form.energia.data,
                "desanimado": form.desanimado.data,
                "esgotado": form.esgotado.data,
                "feliz": form.feliz.data,
                "cansado": form.cansado.data,
            },

            "qld_vida_limitacao": {
                "temp_atv_fis": form.temp_atv_fis.data,
                "qtd_atv_fis": form.qtd_atv_fis.data,
                "limitado_fis": form.limitado_fis.data,
                "dif_fis": form.dif_fis.data,
                "temp_atv_emo": form.temp_atv_emo.data,  
                "qtd_atv_emo": form.qtd_atv_emo.data,
                "cuidado_atv": form.cuidado_atv.data,
                "social": form.social.data,
                "temp_social": form.temp_social.data,
            }
        }

        alteracoes = False
        for tabela, dados in dados_tabelas.items():
                supabase.table(tabela).update(dados).eq("id_estudos_geral", pesquisa['id']).execute()
                alteracoes = True
            
        flash('Pesquisa atualizada com sucesso!', 'info') if alteracoes else flash('Nenhuma alteração foi realizada.', 'secondary')
        return redirect(url_for('pesq.minhas_pesquisas'))
    

    if request.method == 'GET':
        form = FormularioQualidadeVida(data=respostas)
      
    return render_template(
        "pesquisas/qual_vida.html",
        form=form,
        id_entrevistado=pesquisa["id_entrevistado"],
        editar=True,
        id_pesquisa=pesquisa['id']
    )


# ================== ROTA VISUALIZAR QUALIDADE VIDA ADM ===================
@qual_vida_bp.route("/visualizar_qual_vida_admin/<int:id>")
@acesso_admin
@validar_acesso_adm
def visualizar_qual_vida_admin(pesquisa):

    resposta_form = (
        supabase.table("qld_vida_completo")
        .select("*")
        .eq("id", pesquisa['id'])
        .maybe_single()
        .execute()
    )

    respostas = resposta_form.data if resposta_form else None

    if not respostas:
        return redirect(url_for("admin.visualizar_pesquisas"))
    
    dados_form = {
        **respostas
    }

    form = FormularioQualidadeVida(data=dados_form)
    for field in form:
        field.render_kw = {"disabled": True}

    return render_template(
        "pesquisas/qual_vida.html",
        form=form,
        id_entrevistado=pesquisa["id_entrevistado"],
        visualizar=True,
        admin=True
    )

