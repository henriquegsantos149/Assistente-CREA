import re
from flask import Blueprint, request, jsonify
from api.shared.llm import call_openrouter
from api.shared.rag import get_crea_context
from api.crea.prompt import build_crea_system_prompt
from api.shared.db import criar_ou_carregar_sessao, persistir_mensagem

crea_bp = Blueprint('crea_bp', __name__)

@crea_bp.route('/extract-name', methods=['POST'])
def extract_name():
    try:
        dados = request.json
        mensagem_aluno = dados.get("mensagem", "")

        system_prompt = "Sua única função é extrair o NOME do usuário a partir da frase fornecida. Responda APENAS com o nome extraído, com a primeira letra maiúscula. Exemplo: se o usuário disser 'Olá, me chamo João Pedro', responda APENAS 'João Pedro'. Se disser 'sou o marcos', responda 'Marcos'. Não escreva mais nenhuma palavra."

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

@crea_bp.route('/chat', methods=['POST'])
def chat_crea():
    try:
        dados = request.json
        mensagem_aluno = dados.get("mensagem")
        nome = dados.get("nome", "Aluno")
        estado = dados.get("estado", "Desconhecido")
        formacao = dados.get("formacao", "Desconhecida")
        ano = dados.get("ano", "Desconhecido")
        has_crea = dados.get("hasCrea", "Não informado")
        
        # Parâmetros adicionais para memória e persistência
        sessao_id = dados.get("sessao_id")
        historico = dados.get("historico", [])

        # Chama a função de RAG com a pergunta do usuário
        conteudo_documentos_rag = get_crea_context(mensagem_aluno)
        
        # Busca regras customizadas
        regras_customizadas = ""
        try:
            import os
            import requests
            from api.shared.db import _get_active_backend
            backend = _get_active_backend()
            if backend == "supabase":
                url = f"{os.environ.get('SUPABASE_URL', '').rstrip('/')}/rest/v1/configuracoes_agentes?select=regras_customizadas&id=eq.crea"
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
        
        system_prompt = build_crea_system_prompt(nome, estado, formacao, ano, has_crea, conteudo_documentos_rag, regras_customizadas)

        # 1. Tenta criar ou carregar a sessão no Supabase para guardar o perfil
        metadados = {
            "formacao": formacao,
            "ano": ano,
            "has_crea": has_crea,
            "estado": estado
        }
        
        try:
            sessao_db = criar_ou_carregar_sessao(sessao_id, "crea", nome, metadados)
            if sessao_db:
                sessao_id = sessao_db.get("id", sessao_id)
        except Exception as err:
            print(f"[ONBOARDING DB WARNING] Falha ao sincronizar perfil: {err}")

        # 2. Persiste a mensagem de envio do aluno no Supabase
        if sessao_id:
            try:
                persistir_mensagem(sessao_id, "user", mensagem_aluno)
            except Exception as err:
                print(f"[LOG USER MSG WARNING] {err}")
        
        try:
            # Chama o LLM com o histórico
            resposta_texto = call_openrouter(system_prompt, mensagem_aluno, history=historico)
            
            # 3. Persiste a resposta do agente no Supabase
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
