import os
from flask import Blueprint, render_template, redirect, session, url_for, flash, request
from supabase import create_client
from datetime import datetime

from FlaskWTF.pesquisas.coorte_form import FormularioCoorte
from ..pesquisador import limpar_sessao_pesquisa, acesso_pesq, validar_acesso_pesquisa
from ..adm import acesso_admin, validar_acesso_adm


coorte_bp = Blueprint ('coorte', __name__)


supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


# ================== ROTA COLETA DADOS COORTE ===================
@coorte_bp.route('/coleta_dados_coorte/<int:id_entrevistado>', methods=['GET', 'POST'])
def coleta_dados_coorte(id_entrevistado):

    token_url = request.args.get('token')
    token_sessao = session.get('token_pesquisa')

    if not token_url or token_url != token_sessao:
        return redirect(url_for('pesq.pg_pesq'))
    
    form = FormularioCoorte()

    if form.validate_on_submit():
        user_id = session.get('id_usuario')

        estudos_geral_data = {
            'id_entrevistado': id_entrevistado, 
            'id_usuario': user_id, 
            'data_horario': datetime.now().isoformat(),
            'tipo': 'Coorte'
        }

        response_estudo = supabase.table('estudos_geral').insert(estudos_geral_data).execute()
    
        _id = response_estudo.data[0]['id']

        sinais_vitais_data = {
            'id_estudos_geral': _id,
            'pa': form.pa.data,
            'fc': form.fc.data,
            'saturacao': form.saturacao.data,
        }

        testes_motores_data = {
            'id_estudos_geral': _id,
            'timed_up_go_1': form.timed_up_go_1.data,
            'timed_up_go_2': form.timed_up_go_2.data,
            'timed_up_go_3': form.timed_up_go_3.data,
            'chair_test': form.chair_test.data,
            'pren_man_dir_1': form.pren_man_dir_1.data,
            'pren_man_dir_2': form.pren_man_dir_2.data,
            'pren_man_dir_3': form.pren_man_dir_3.data,
            'pren_man_esq_1': form.pren_man_esq_1.data,
            'pren_man_esq_2': form.pren_man_esq_2.data,
            'pren_man_esq_3': form.pren_man_esq_3.data,
        }

        antropometria_data = {
            'id_estudos_geral': _id,
            'massa': form.massa.data,
            'estatura': form.estatura.data,
            'esp_polegar': form.esp_polegar.data,
            'quadril': form.quadril.data,
            'abdomen': form.abdomen.data,
            'antebraco_dir': form.antebraco_dir.data,
            'antebraco_esq': form.antebraco_esq.data,
            'braco_rel_dir': form.braco_rel_dir.data,
            'braco_rel_esq': form.braco_rel_esq.data,
            'braco_ctr_dir': form.braco_ctr_dir.data,
            'braco_ctr_esq': form.braco_ctr_esq.data,
            'panturrilha_dir': form.panturrilha_dir.data,
            'panturrilha_esq': form.panturrilha_esq.data,
            'coxa_sup_dir': form.coxa_sup_dir.data,
            'coxa_sup_esq': form.coxa_sup_esq.data,
        }

        supabase.table('sinais_vitais').insert(sinais_vitais_data).execute()
        supabase.table('testes_motores').insert(testes_motores_data).execute()
        supabase.table('antropometria').insert(antropometria_data).execute()

        limpar_sessao_pesquisa()

        flash('Formulário registrado com sucesso!', 'info')
        return redirect(url_for('pesq.nova_pesquisa'))

    return render_template('pesquisas/coorte.html', form=form, id_entrevistado=id_entrevistado)


# ================== ROTA VISUALIZAR DADOS COORTE ===================
@coorte_bp.route("/visualizar_coorte/<int:id>")
@acesso_pesq
@validar_acesso_pesquisa
def visualizar_coorte(pesquisa):

    resposta_form = (
        supabase.table("coorte_completo")
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

    form = FormularioCoorte(data=dados_form)
    for field in form:
        field.render_kw = {"disabled": True}

    return render_template(
        "pesquisas/coorte.html",
        form=form,
        id_entrevistado=pesquisa["id_entrevistado"],
        visualizar=True
    )


# ================== ROTA EDITAR DADOS COORTE ===================
@coorte_bp.route("/editar_coorte/<int:id>", methods=['GET', 'POST'])
@acesso_pesq
@validar_acesso_pesquisa
def editar_coorte(pesquisa):

    resposta_form = (
        supabase.table("coorte_completo")
        .select("*")
        .eq("id", pesquisa['id'])
        .maybe_single()
        .execute()
    )
     
    respostas = resposta_form.data if resposta_form else None

    if not respostas:
        return redirect(url_for("pesq.minhas_pesquisas"))

    form = FormularioCoorte()

    if form.validate_on_submit():
        
        dados_tabelas = {
            'sinais_vitais': {
                'pa': form.pa.data,
                'fc': form.fc.data,
                'saturacao': form.saturacao.data
            },

            'testes_motores': {
                'timed_up_go_1': form.timed_up_go_1.data,
                'timed_up_go_2': form.timed_up_go_2.data,
                'timed_up_go_3': form.timed_up_go_3.data,
                'chair_test': form.chair_test.data,
                'pren_man_dir_1': form.pren_man_dir_1.data,
                'pren_man_dir_2': form.pren_man_dir_2.data,
                'pren_man_dir_3': form.pren_man_dir_3.data,
                'pren_man_esq_1': form.pren_man_esq_1.data,
                'pren_man_esq_2': form.pren_man_esq_2.data,
                'pren_man_esq_3': form.pren_man_esq_3.data,
            },

            'antropometria': {
            
                'massa': form.massa.data,
                'estatura': form.estatura.data,
                'esp_polegar': form.esp_polegar.data,
                'quadril': form.quadril.data,
                'abdomen': form.abdomen.data,
                'antebraco_dir': form.antebraco_dir.data,
                'antebraco_esq': form.antebraco_esq.data,
                'braco_rel_dir': form.braco_rel_dir.data,
                'braco_rel_esq': form.braco_rel_esq.data,
                'braco_ctr_dir': form.braco_ctr_dir.data,
                'braco_ctr_esq': form.braco_ctr_esq.data,
                'panturrilha_dir': form.panturrilha_dir.data,
                'panturrilha_esq': form.panturrilha_esq.data,
                'coxa_sup_dir': form.coxa_sup_dir.data,
                'coxa_sup_esq': form.coxa_sup_esq.data,
            }
            
        }

        alteracoes = False
        for tabela, dados in dados_tabelas.items():
            supabase.table(tabela).update(dados).eq("id_estudos_geral", pesquisa['id']).execute()
            alteracoes = True

        flash('Pesquisa atualizada com sucesso!', 'info') if alteracoes else flash('Nenhuma alteração foi realizada.', 'secondary')
        return redirect(url_for('pesq.minhas_pesquisas'))
    
    if request.method == 'GET':
        form = FormularioCoorte(data=respostas)

    return render_template(
        "pesquisas/coorte.html",
        form=form,
        id_entrevistado=pesquisa["id_entrevistado"],
        editar=True,
        id_pesquisa=pesquisa['id']
    )


# ================== ROTA VISUALIZAR DADOS COORTE ADM ===================
@coorte_bp.route("/visualizar_coorte_admin/<int:id>")
@acesso_admin
@validar_acesso_adm
def visualizar_coorte_admin(pesquisa):

    resposta_form = (
        supabase.table("coorte_completo")
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

    form = FormularioCoorte(data=dados_form)
    for field in form:
        field.render_kw = {"disabled": True}

    return render_template(
        "pesquisas/coorte.html",
        form=form,
        id_entrevistado=pesquisa["id_entrevistado"],
        visualizar=True,
        admin=True
    )