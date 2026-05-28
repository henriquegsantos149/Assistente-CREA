import os
import logging
import re

from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# ⚠️ load_dotenv() DEVE ser chamado ANTES de importar qualquer blueprint
# para garantir que os módulos shared (db.py, llm.py etc.) leiam as
# variáveis de ambiente corretamente no momento do import.
load_dotenv()

# Configuração de logging estruturado
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Importação dos Blueprints
from api.crea.routes import crea_bp
from api.admin.routes import admin_bp

app = Flask(__name__)

# Libera o acesso restrito aos domínios permitidos
origens_permitidas = [
    "http://localhost:5000",
    "http://localhost:8080",
    "http://127.0.0.1:5000",
    "http://127.0.0.1:8080",
    "https://ambientalpro.com.br",
    "https://www.ambientalpro.com.br",
    re.compile(r"https://.*\.vercel\.app$"),
]

CORS(app, resources={r"/*": {"origins": origens_permitidas}})

# Registro dos Blueprints
app.register_blueprint(crea_bp, url_prefix="/api/crea")
app.register_blueprint(admin_bp, url_prefix="/api/admin")

# TODO: Futuros Blueprints (Geo, Experts, Secretaria)
# app.register_blueprint(geo_bp, url_prefix='/api/geo')
# app.register_blueprint(experts_bp, url_prefix='/api/experts')
# app.register_blueprint(secretaria_bp, url_prefix='/api/secretaria')


@app.route("/api/health", methods=["GET"])
def health_check():
    """Endpoint de saúde — retorna status da aplicação e backend de DB ativo."""
    db_backend = os.environ.get("DATABASE_BACKEND", "sqlite")
    return jsonify({
        "status": "ok",
        "version": "1.3",
        "db_backend": db_backend,
    })


@app.errorhandler(404)
def not_found(error):
    return jsonify({"erro": "Rota não encontrada.", "codigo": 404}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"erro": "Método HTTP não permitido.", "codigo": 405}), 405


@app.errorhandler(500)
def internal_error(error):
    logging.error("Erro interno do servidor: %s", error)
    return jsonify({"erro": "Erro interno do servidor. Tente novamente.", "codigo": 500}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))