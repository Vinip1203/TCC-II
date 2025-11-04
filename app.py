import os
from flask import Flask, redirect
from flask_session import Session
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo.env
load_dotenv()

# =============================================================================
# REGISTRO DE BLUEPRINTS - ORGANIZAÇÃO MODULAR DA APLICAÇÃO
# (IMPORTANTE: Importar ANTES das configurações que usam as rotas)
# =============================================================================
from routes.auth import auth_bp 
from routes.adm import admin_bp 
from routes.pesquisador import pesq_bp
from routes.perfil import perfil_bp
from routes.dashboard import dashboard_bp

from routes.pesquisas.alimentacao import alimentacao_bp
from routes.pesquisas.ansiedade import ansiedade_bp
from routes.pesquisas.sarcopenia import sarcopenia_bp
from routes.pesquisas.atv_fisica import atv_fisica_bp
from routes.pesquisas.coorte import coorte_bp
from routes.pesquisas.qual_vida import qual_vida_bp
from routes.pesquisas.vida_saude import vida_saude_bp
from routes.pesquisas.meem import meem_bp

# =============================================================================
# CONFIGURAÇÕES PRINCIPAIS DA APLICAÇÃO FLASK
# =============================================================================
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config["PERMANENT_SESSION_LIFETIME"] = 3600  # ← CORRIGIDO: 1 hora em segundos
app.config["SESSION_TYPE"] = "filesystem"
app.config['WTF_CSRF_ENABLED'] = True

# Para produção no Railway, mude para:
app.config["SESSION_TYPE"] = "null"  # ← SESSÕES DESATIVADAS TEMPORARIAMENTE

Session(app)

# =============================================================================
# REGISTRO DE BLUEPRINTS 
# =============================================================================
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(pesq_bp)
app.register_blueprint(perfil_bp)
app.register_blueprint(dashboard_bp)

app.register_blueprint(alimentacao_bp)
app.register_blueprint(ansiedade_bp)
app.register_blueprint(sarcopenia_bp)
app.register_blueprint(atv_fisica_bp)
app.register_blueprint(coorte_bp)
app.register_blueprint(qual_vida_bp)
app.register_blueprint(vida_saude_bp)
app.register_blueprint(meem_bp)

# =============================================================================
# INICIALIZAÇÃO
# =============================================================================
@app.route("/")
def index():
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=False)  # ← DEBUG DESLIGADO para produção