import os
import json
from flask import Blueprint, render_template, redirect, session, url_for, flash, request
from supabase import create_client
from datetime import datetime

from FlaskWTF.pesquisas.vida_saude_form import FormularioVidaSaude
from ..pesquisador import limpar_sessao_pesquisa, acesso_pesq, validar_acesso_pesquisa
from ..adm import acesso_admin, validar_acesso_adm


vida_saude_bp = Blueprint('vida_saude', __name__)


supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


# ================== ROTA COLETA DADOS VIDA E SAÚDE ===================
@vida_saude_bp.route('/coleta_dados_vida_saude/<int:id_entrevistado>', methods=['GET', 'POST'])
def coleta_dados_vida_saude(id_entrevistado):

    token_url = request.args.get('token')
    token_sessao = session.get('token_pesquisa')

    if not token_url or token_url != token_sessao:
        return redirect(url_for('pesq.pg_pesq'))

    form = FormularioVidaSaude()

    if form.validate_on_submit():
        user_id = session.get('id_usuario')

        estudos_geral_data = {
            'id_entrevistado': id_entrevistado, 
            'id_usuario': user_id, 
            'data_horario': datetime.now().isoformat(),
            'tipo': 'Vida e Saúde'
        }

        response_estudo = supabase.table('estudos_geral').insert(estudos_geral_data).execute()

        _id = response_estudo.data[0]['id']

        info_pessoais_data = {
            'id_estudos_geral': _id,
            'data_nasc': form.data_nasc.data.isoformat(),
            'sexo': form.sexo.data,
            'pele': form.pele.data,
            'local_nasc': form.local_nasc.data,
            'cidade': form.cidade.data,
            'estado': form.estado.data,
            'pais': form.pais.data,
            'local_resid': form.local_resid.data,
            'tempo_resid': form.tempo_resid.data,
            'estado_civil': form.estado_civil.data,
            'escolaridade': form.escolaridade.data,
            'aposentadoria': form.aposentadoria.data,
            'valor_apos': form.valor_apos.data,
        }

        moradia_data = {
            'id_estudos_geral': _id,
            'casa': form.casa.data,
            'esgoto': form.esgoto.data,
            'luz': form.luz.data,
            'lixo': form.lixo.data,
            'meios_transporte': form.meios_transporte.data,
        }


        composicao_familiar_data = {
            'id_estudos_geral': _id,
            'modo_vida': form.modo_vida.data,
            'satisf_vida': form.satisf_vida.data,
        }

        condicao_saude_data = {
            'id_estudos_geral': _id,
            'medicamentos': form.Medicamentos.data,
            'motivo_uso': form.motivo_uso.data,
            'aquisicao': form.aquisicao.data,
            'saude_geral': form.saude_geral.data,
        }

        problemas_saude_data = {
            'id_estudos_geral': _id,
            'reumatismo': form.reumatismo.data,
            'asma_bronquite': form.asma_bronquite.data,
            'pressao_alta': form.pressao_alta.data,
            'varizes': form.varizes.data,
            'diabetes': form.diabetes.data,
            'obesidade': form.obesidade.data,
            'derrame': form.derrame.data,
            'incontinencia': form.incontinencia.data,
            'prisao_ventre': form.prisao_ventre.data,
            'insonia': form.insonia.data,
            'catarata': form.catarata.data,
            'problema_coluna': form.problema_coluna.data,
            'artrite_artrose': form.artrite_artrose.data,
            'osteoporose': form.osteoporose.data,
            'nervos': form.nervos.data,
            'tuberculose': form.tuberculose.data,
            'cardiaco': form.cardiaco.data,
            'anemia': form.anemia.data,
            'parkinson': form.parkinson.data,
            'cancer': form.cancer.data,
            'alzheimer': form.alzheimer.data,
            'depressao': form.depressao.data,
            'osteomioarticulares': form.osteomioarticulares.data,
            'tontura': form.tontura.data,
            'colesterol': form.colesterol.data,
            'constipacao': form.constipacao.data,
        }

        apoio_familiar_social_data = {
            'id_estudos_geral': _id,
            'cuidador': form.cuidador.data,
            'idade_cuidador': form.idade_cuidador.data,
            'sexo_cuidador': form.sexo_cuidador.data,
            'servico_saude': form.servico_saude.data,
        }

        supabase.table('info_pessoais').insert(info_pessoais_data).execute()
        supabase.table('moradia').insert(moradia_data).execute()
        supabase.table('composicao_familiar').insert(composicao_familiar_data).execute()
        supabase.table('condicao_saude').insert(condicao_saude_data).execute()
        supabase.table('problemas_saude').insert(problemas_saude_data).execute()
        supabase.table('apoio_familiar_social').insert(apoio_familiar_social_data).execute()

        limpar_sessao_pesquisa()

        flash('Formulário registrado com sucesso!', 'info')
        return redirect(url_for('pesq.nova_pesquisa'))

    return render_template('pesquisas/vida_saude.html', form=form, id_entrevistado=id_entrevistado)


# ================== ROTA VISUALIZAR DADOS VIDA E SAÚDE ===================
@vida_saude_bp.route("/visualizar_vida_saude/<int:id>")
@acesso_pesq
@validar_acesso_pesquisa
def visualizar_vida_saude(pesquisa):

    resposta_form = (
        supabase.table("vida_saude_completo")
        .select("*")
        .eq("id", pesquisa['id'])
        .maybe_single()
        .execute()
    )

    respostas = resposta_form.data if resposta_form else None

    if not respostas:
        return redirect(url_for("pesq.minhas_pesquisas"))
    
    dados_form = {
        **respostas,
        "data_nasc": datetime.fromisoformat(respostas['data_nasc']).date(),
        "meios_transporte": json.loads(respostas["meios_transporte"]),
        "cuidador": json.loads(respostas["cuidador"]),
        "servico_saude": json.loads(respostas["servico_saude"]),
        "Medicamentos": respostas["medicamentos"]
    }

    form = FormularioVidaSaude(data=dados_form)
    for field in form:
        field.render_kw = {"disabled": True}

    return render_template(
        "pesquisas/vida_saude.html",
        form=form,
        id_entrevistado=pesquisa["id_entrevistado"],
        visualizar=True
    )


# ================== ROTA EDITAR VIDA E SAÚDE ===================
@vida_saude_bp.route("/editar_vida_saude/<int:id>", methods=['GET', 'POST'])
@acesso_pesq
@validar_acesso_pesquisa
def editar_vida_saude(pesquisa):

    resposta_form = (
        supabase.table("vida_saude_completo")
        .select("*")
        .eq("id", pesquisa['id'])
        .maybe_single()
        .execute()
    )
     
    respostas = resposta_form.data if resposta_form else None

    if not respostas:
        return redirect(url_for("pesq.minhas_pesquisas"))

    form = FormularioVidaSaude()

    if form.validate_on_submit():
        
        dados_tabelas = {

            'info_pessoais':{
                'data_nasc': form.data_nasc.data.isoformat(),
                'sexo': form.sexo.data,
                'pele': form.pele.data,
                'local_nasc': form.local_nasc.data,
                'cidade': form.cidade.data,
                'estado': form.estado.data,
                'pais': form.pais.data,
                'local_resid': form.local_resid.data,
                'tempo_resid': form.tempo_resid.data,
                'estado_civil': form.estado_civil.data,
                'escolaridade': form.escolaridade.data,
                'aposentadoria': form.aposentadoria.data,
                'valor_apos': form.valor_apos.data,
            },

            'moradia': {
                'casa': form.casa.data,
                'esgoto': form.esgoto.data,
                'luz': form.luz.data,
                'lixo': form.lixo.data,
                'meios_transporte': form.meios_transporte.data,
            },

            'composicao_familiar': {
                'modo_vida': form.modo_vida.data,
                'satisf_vida': form.satisf_vida.data,
            },

            'condicao_saude': {
                'medicamentos': form.Medicamentos.data,
                'motivo_uso': form.motivo_uso.data,
                'aquisicao': form.aquisicao.data,
                'saude_geral': form.saude_geral.data,
            },

            'problemas_saude': {
                'reumatismo': form.reumatismo.data,
                'asma_bronquite': form.asma_bronquite.data,
                'pressao_alta': form.pressao_alta.data,
                'varizes': form.varizes.data,
                'diabetes': form.diabetes.data,
                'obesidade': form.obesidade.data,
                'derrame': form.derrame.data,
                'incontinencia': form.incontinencia.data,
                'prisao_ventre': form.prisao_ventre.data,
                'insonia': form.insonia.data,
                'catarata': form.catarata.data,
                'problema_coluna': form.problema_coluna.data,
                'artrite_artrose': form.artrite_artrose.data,
                'osteoporose': form.osteoporose.data,
                'nervos': form.nervos.data,
                'tuberculose': form.tuberculose.data,
                'cardiaco': form.cardiaco.data,
                'anemia': form.anemia.data,
                'parkinson': form.parkinson.data,
                'cancer': form.cancer.data,
                'alzheimer': form.alzheimer.data,
                'depressao': form.depressao.data,
                'osteomioarticulares': form.osteomioarticulares.data,
                'tontura': form.tontura.data,
                'colesterol': form.colesterol.data,
                'constipacao': form.constipacao.data,
            },

            'apoio_familiar_social': {
                'cuidador': form.cuidador.data,
                'idade_cuidador': form.idade_cuidador.data,
                'sexo_cuidador': form.sexo_cuidador.data,
                'servico_saude': form.servico_saude.data,
            }
        }

        alteracoes = False
        for tabela, dados in dados_tabelas.items():
            supabase.table(tabela).update(dados).eq("id_estudos_geral", pesquisa['id']).execute()
            alteracoes = True

        flash('Pesquisa atualizada com sucesso!', 'info') if alteracoes else flash('Nenhuma alteração foi realizada.', 'secondary')
        return redirect(url_for('pesq.minhas_pesquisas'))
    
    if request.method == 'GET':
        form = FormularioVidaSaude(data={
            **respostas,
            "data_nasc": datetime.fromisoformat(respostas['data_nasc']).date(),
            "meios_transporte": json.loads(respostas["meios_transporte"]),
            "cuidador": json.loads(respostas["cuidador"]),
            "servico_saude": json.loads(respostas["servico_saude"]),
            "Medicamentos": respostas["medicamentos"]
        })

    return render_template(
        "pesquisas/vida_saude.html",
        form=form,
        id_entrevistado=pesquisa["id_entrevistado"],
        editar=True,
        id_pesquisa=pesquisa['id']
    )


# ================== ROTA VISUALIZAR DADOS VIDA E SAÚDE ADM ===================
@vida_saude_bp.route("/visualizar_vida_saude_admin/<int:id>")
@acesso_admin
@validar_acesso_adm
def visualizar_vida_saude_admin(pesquisa):

    resposta_form = (
        supabase.table("vida_saude_completo")
        .select("*")
        .eq("id", pesquisa['id'])
        .maybe_single()
        .execute()
    )

    respostas = resposta_form.data if resposta_form else None

    if not respostas:
        return redirect(url_for("admin.visualizar_pesquisas"))
    
    dados_form = {
        **respostas,
        "data_nasc": datetime.fromisoformat(respostas['data_nasc']).date(),
        "meios_transporte": json.loads(respostas["meios_transporte"]),
        "cuidador": json.loads(respostas["cuidador"]),
        "servico_saude": json.loads(respostas["servico_saude"]),
        "Medicamentos": respostas["medicamentos"]
    }

    form = FormularioVidaSaude(data=dados_form)
    for field in form:
        field.render_kw = {"disabled": True}

    return render_template(
        "pesquisas/vida_saude.html",
        form=form,
        id_entrevistado=pesquisa["id_entrevistado"],
        visualizar=True,
        admin=True
    )

