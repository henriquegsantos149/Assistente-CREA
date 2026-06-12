import os
import re
import json
import base64
import requests
import fitz

from flask import Blueprint, request, jsonify
from api.shared.llm import call_openrouter
from api.portfolio_geo.prompt import build_portfolio_system_prompt
from api.shared.db import criar_ou_carregar_sessao, persistir_mensagem, _get_active_backend

portfolio_geo_bp = Blueprint('portfolio_geo_bp', __name__)

@portfolio_geo_bp.route('/extract-name', methods=['POST'])
def extract_name():
    try:
        dados = request.json
        mensagem_aluno = dados.get("mensagem", "")

        system_prompt = "Sua única função é extrair o NOME do usuário EXATAMENTE como foi escrito na frase, sem alterar ou corrigir a ortografia (por exemplo, mantenha 'Manoel' com O se estiver escrito assim). Apenas ajuste a primeira letra para maiúscula. Responda APENAS com o nome extraído. Exemplo: se o usuário disser 'Olá, me chamo João Pedro', responda APENAS 'João Pedro'. Se disser 'sou o marcos', responda 'Marcos'. Não escreva mais nenhuma palavra."

        try:
            resposta_texto = call_openrouter(system_prompt, mensagem_aluno, max_tokens=10, temperature=0.1)
            resposta_texto = resposta_texto.replace(".", "").replace("!", "").strip()
        except Exception as e:
            resposta_texto = ""

        if not resposta_texto or len(resposta_texto.split()) > 3 or "meu nome" in resposta_texto.lower() or "me chamo" in resposta_texto.lower():
            limpo = mensagem_aluno
            while True:
                novo_limpo = re.sub(r"^(eu sou o|eu sou a|eu me chamo|sou o|sou a|sou|me chamo|meu nome [eé]|o meu nome [eé]|ol[aá]|ola|bom dia|boa tarde|boa noite|pode me chamar de)[\s,]+", "", limpo, flags=re.IGNORECASE).strip()
                if novo_limpo == limpo:
                    break
                limpo = novo_limpo
            
            palavras = limpo.split()
            if palavras:
                resposta_texto = " ".join([p.capitalize() for p in palavras[:2]])
            else:
                resposta_texto = mensagem_aluno

        return jsonify({"nome": resposta_texto}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@portfolio_geo_bp.route('/chat', methods=['POST'])
def chat_portfolio():
    try:
        dados = request.form if request.files else request.json
        if not dados and request.form:
            dados = request.form
            
        mensagem_aluno = dados.get("mensagem", "")
        nome = dados.get("nome", "Aluno")
        estado = dados.get("estado", "Desconhecido")
        formacao = dados.get("formacao", "Desconhecida")
        ano = dados.get("ano", "Desconhecido")
        has_crea = dados.get("hasCrea", "Não informado")
        
        sessao_id = dados.get("sessao_id")
        historico_str = dados.get("historico", "[]")
        if isinstance(historico_str, str):
            try:
                historico = json.loads(historico_str)
            except:
                historico = []
        else:
            historico = historico_str

        file = request.files.get("file") if request.files else None
        
        image_contents = []

        if file:
            filename = file.filename.lower()
            if filename.endswith(".pdf"):
                try:
                    pdf_bytes = file.read()
                    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
                    num_pages = min(3, len(pdf_document))
                    for i in range(num_pages):
                        page = pdf_document.load_page(i)
                        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                        img_bytes = pix.tobytes("png")
                        base64_img = base64.b64encode(img_bytes).decode("utf-8")
                        image_contents.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_img}"
                            }
                        })
                    pdf_document.close()
                except Exception as e:
                    print(f"[PDF EXTRACTION ERROR] {e}")
            elif filename.endswith((".png", ".jpg", ".jpeg")):
                try:
                    mime_type = "image/png" if filename.endswith(".png") else "image/jpeg"
                    base64_img = base64.b64encode(file.read()).decode("utf-8")
                    image_contents.append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_img}"
                        }
                    })
                except Exception as e:
                    print(f"[IMAGE ENCODE ERROR] {e}")

        regras_customizadas = ""
        try:
            backend = _get_active_backend()
            if backend == "supabase":
                url = f"{os.environ.get('SUPABASE_URL', '').rstrip('/')}/rest/v1/configuracoes_agentes?select=regras_customizadas&id=eq.portfolio"
                key = os.environ.get("SUPABASE_KEY", "")
                if url and key:
                    headers = {"apikey": key, "Authorization": f"Bearer {key}", "Content-Type": "application/json"}
                    res = requests.get(url, headers=headers, timeout=5)
                    if res.status_code == 200:
                        data = res.json()
                        if data and len(data) > 0:
                            regras_customizadas = data[0].get("regras_customizadas", "")
        except Exception as err:
            print(f"[RULES WARNING] Falha ao buscar regras customizadas: {err}")
        
        system_prompt = build_portfolio_system_prompt(nome, estado, formacao, ano, has_crea, "", regras_customizadas)

        metadados = {
            "formacao": formacao,
            "ano": ano,
            "has_crea": has_crea,
            "estado": estado
        }
        
        try:
            sessao_db = criar_ou_carregar_sessao(sessao_id, "portfolio", nome, metadados)
            if sessao_db:
                sessao_id = sessao_db.get("id", sessao_id)
        except Exception as err:
            print(f"[ONBOARDING DB WARNING] Falha ao sincronizar perfil: {err}")

        if sessao_id:
            try:
                persistir_mensagem(sessao_id, "user", mensagem_aluno)
            except Exception as err:
                print(f"[LOG USER MSG WARNING] {err}")
        
        user_content_for_llm = mensagem_aluno
        if image_contents:
            user_content_for_llm = [{"type": "text", "text": mensagem_aluno}]
            user_content_for_llm.extend(image_contents)
            
        try:
            resposta_texto = call_openrouter(system_prompt, user_content_for_llm, history=historico)
            
            if sessao_id:
                try:
                    persistir_mensagem(sessao_id, "agent", resposta_texto)
                except Exception as err:
                    print(f"[LOG AGENT MSG WARNING] {err}")
                    
            return jsonify({
                "resposta": resposta_texto,
                "sessao_id": sessao_id
            }), 200
        except Exception as e:
            return jsonify({"erro": str(e)}), 500

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
