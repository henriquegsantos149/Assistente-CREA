import csv
import io
import json
import requests
import os
import subprocess
from werkzeug.utils import secure_filename
from flask import Blueprint, jsonify, Response, request
from api.shared.db import obter_todas_mensagens
from api.shared.llm import call_openrouter

admin_bp = Blueprint('admin_bp', __name__)

def parse_chat_history(mensagens):
    """
    Agrupa mensagens em pares (Pergunta do Aluno, Resposta da IA)
    baseado na ordem cronológica (mais antigas primeiro).
    """
    mensagens = sorted(mensagens, key=lambda m: m['created_at'])
    
    pares = []
    pergunta_atual = None
    
    for msg in mensagens:
        if msg['sender'] == 'user':
            pergunta_atual = msg
        elif msg['sender'] == 'agent' and pergunta_atual:
            pares.append({
                'data': pergunta_atual['created_at'],
                'nome': pergunta_atual.get('user_nome', 'Desconhecido'),
                'pergunta': pergunta_atual.get('content', ''),
                'resposta': msg.get('content', '')
            })
            pergunta_atual = None
            
    # Se sobrou uma pergunta sem resposta no final
    if pergunta_atual:
        pares.append({
            'data': pergunta_atual['created_at'],
            'nome': pergunta_atual.get('user_nome', 'Desconhecido'),
            'pergunta': pergunta_atual.get('content', ''),
            'resposta': '(Sem resposta)'
        })
        
    # Retorna do mais recente para o mais antigo
    return sorted(pares, key=lambda x: x['data'], reverse=True)


@admin_bp.route('/export-prompts', methods=['GET'])
def export_prompts():
    try:
        raw_mensagens = obter_todas_mensagens()
        pares = parse_chat_history(raw_mensagens)
        
        si = io.StringIO()
        cw = csv.writer(si, delimiter=';')
        # Cabeçalho aprovado pelo usuário
        cw.writerow(['Data', 'Nome do Aluno', 'Pergunta do Aluno', 'Resposta da IA'])
        
        for par in pares:
            cw.writerow([par['data'], par['nome'], par['pergunta'], par['resposta']])
            
        output = si.getvalue()
        
        return Response(
            output,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=prompts_alunos.csv"}
        )
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@admin_bp.route('/insights', methods=['POST'])
def gerar_insights():
    try:
        raw_mensagens = obter_todas_mensagens()
        pares = parse_chat_history(raw_mensagens)
        
        if not pares:
            return jsonify({"insight": "Não há dados suficientes no histórico para gerar insights."}), 200
            
        # Pega as últimas 50 interações para análise (evitar limite de tokens)
        ultimos_pares = pares[:50]
        texto_analise = ""
        for i, par in enumerate(ultimos_pares):
            texto_analise += f"Interação {i+1}:\nAluno ({par['nome']}): {par['pergunta']}\n\n"
            
        system_prompt = (
            "Você é o 'Analista de Dados' oficial da plataforma CRE.IA. "
            "Sua missão é analisar o histórico de perguntas dos alunos e fornecer Insights valiosos "
            "para o administrador da plataforma.\n"
            "Analise as interações abaixo e escreva um relatório curto em formato Markdown abordando:\n"
            "1. Principais temas e dúvidas frequentes.\n"
            "2. Onde os alunos demonstram mais dificuldade.\n"
            "3. Sugestões de melhoria (ex: materiais extras que podem ser criados baseados nas dúvidas).\n"
            "Seja profissional, direto e use formatação limpa (listas e negritos)."
        )
        
        resposta = call_openrouter(system_prompt, texto_analise, max_tokens=1500, temperature=0.3)
        
        return jsonify({"insight": resposta}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


import os
from pathlib import Path

@admin_bp.route('/config', methods=['GET'])
def get_config():
    try:
        from dotenv import load_dotenv
        env_path = Path(__file__).parent.parent.parent / '.env'
        load_dotenv(dotenv_path=env_path)

        supabase_url = os.environ.get("SUPABASE_URL", "").rstrip('/')
        supabase_key = os.environ.get("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            return jsonify({"models": [], "agent_configs": {}}), 200

        headers = {
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}",
            "Content-Type": "application/json"
        }

        url = f"{supabase_url}/rest/v1/configuracoes_agentes?select=*"
        res = requests.get(url, headers=headers, timeout=10)
        
        config = {"models": [], "agent_configs": {}}
        
        if res.status_code == 200:
            data = res.json()
            for row in data:
                row_id = row.get("id")
                if row_id == "global":
                    config["models"] = row.get("modelos_fallback", [])
                else:
                    config["agent_configs"][row_id] = {
                        "regras_customizadas": row.get("regras_customizadas", "")
                    }
        
        return jsonify(config), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@admin_bp.route('/config', methods=['POST'])
def save_config():
    try:
        dados = request.json
        
        from dotenv import load_dotenv
        env_path = Path(__file__).parent.parent.parent / '.env'
        load_dotenv(dotenv_path=env_path)

        supabase_url = os.environ.get("SUPABASE_URL", "").rstrip('/')
        supabase_key = os.environ.get("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            return jsonify({"erro": "Credenciais Supabase não configuradas no servidor."}), 500

        headers = {
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates"
        }
        
        url = f"{supabase_url}/rest/v1/configuracoes_agentes"
        
        # Salva o global (modelos)
        models = dados.get("models", [])
        payload_global = {
            "id": "global",
            "modelos_fallback": models
        }
        requests.post(url, json=payload_global, headers=headers, timeout=10)
        
        # Salva os agentes
        agent_configs = dados.get("agent_configs", {})
        for agent_id, agent_data in agent_configs.items():
            payload_agent = {
                "id": agent_id,
                "regras_customizadas": agent_data.get("regras_customizadas", "")
            }
            requests.post(url, json=payload_agent, headers=headers, timeout=10)

        return jsonify({"status": "sucesso"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@admin_bp.route('/openrouter-models', methods=['GET'])
def list_openrouter_models():
    """Busca a lista de modelos atualizados da OpenRouter"""
    try:
        # A API da OpenRouter para listar modelos é aberta, não precisa de chave,
        # mas vamos passar para evitar qualquer bloqueio
        headers = {}
        # Opcional: Se quiser usar a chave:
        # from api.shared.llm import get_openrouter_key
        # key = get_openrouter_key()
        # if key: headers['Authorization'] = f'Bearer {key}'
        
        response = requests.get('https://openrouter.ai/api/v1/models', headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            models = []
            for m in data.get('data', []):
                models.append({
                    "id": m.get('id'),
                    "name": m.get('name')
                })
            # Ordenar por nome
            models.sort(key=lambda x: x['name'])
            return jsonify({"models": models})
        else:
            return jsonify({"erro": "Falha ao buscar modelos"}), 500
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@admin_bp.route('/upload-rag', methods=['POST'])
def upload_rag_pdf():
    """Recebe um PDF e processa a vetorização via script Node.js."""
    try:
        if 'file' not in request.files:
            return jsonify({"erro": "Nenhum arquivo enviado"}), 400
        
        file = request.files['file']
        agent_table = request.form.get('agentTable')

        if file.filename == '':
            return jsonify({"erro": "Nome do arquivo vazio"}), 400
            
        if not agent_table:
            return jsonify({"erro": "Agente/Tabela não informada"}), 400

        # Salvar arquivo temporariamente
        filename = secure_filename(file.filename)
        # Vamos salvar na pasta 'Documentos'
        upload_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'Documentos')
        os.makedirs(upload_dir, exist_ok=True)
        filepath = os.path.join(upload_dir, filename)
        file.save(filepath)

        # Chamar script Node
        node_script = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'vetorizador', 'processar_pdf.mjs')
        
        # Como o subprocess é bloqueante e pode demorar, vamos aguardar para ter o resultado.
        # Em produção, idealmente seria async/fila, mas para dashboard admin está OK.
        result = subprocess.run(['node', node_script, filepath, agent_table], capture_output=True, text=True)
        
        if result.returncode == 0:
            return jsonify({"status": "sucesso", "log": result.stdout})
        else:
            return jsonify({"erro": "Erro na vetorização", "detalhes": result.stderr}), 500

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@admin_bp.route('/chat-history', methods=['GET'])
def get_chat_history():
    """Retorna as sessões mais recentes agrupadas por ID."""
    try:
        mensagens = obter_todas_mensagens()
        
        # Agrupar por sessao
        sessoes = {}
        for msg in mensagens:
            sid = msg.get('session_id')
            if sid not in sessoes:
                sessoes[sid] = {
                    "session_id": sid,
                    "data": msg.get('timestamp'),
                    "usuario": "Usuário Anônimo",
                    "primeira_pergunta": "",
                    "mensagens": []
                }
            sessoes[sid]['mensagens'].append(msg)
            
            # Tentar achar a primeira pergunta de usuário
            if msg.get('role') == 'user' and not sessoes[sid]['primeira_pergunta']:
                sessoes[sid]['primeira_pergunta'] = msg.get('content')
                
        # Organizar numa lista
        lista_sessoes = list(sessoes.values())
        
        # Ordenar por data decrescente
        lista_sessoes.sort(key=lambda x: x['data'], reverse=True)
        
        # Limitar as 15 últimas para não pesar
        return jsonify({"sessoes": lista_sessoes[:15]}), 200
        
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@admin_bp.route('/rag-files', methods=['GET'])
def get_rag_files():
    """Retorna a lista de arquivos únicos que já foram vetorizados para um dado agente."""
    try:
        agent_table = request.args.get('agentTable')
        if not agent_table:
            return jsonify({"erro": "Agente/Tabela não informada"}), 400

        # Garantir que o .env está carregado caso o flask não tenha rodado da raiz
        from dotenv import load_dotenv
        env_path = Path(__file__).parent.parent.parent / '.env'
        load_dotenv(dotenv_path=env_path)

        supabase_url = os.environ.get("SUPABASE_URL")
        supabase_key = os.environ.get("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            return jsonify({"erro": "Credenciais Supabase não configuradas no servidor."}), 500

        supabase_url = supabase_url.rstrip('/')

        headers = {
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}",
            "Content-Type": "application/json"
        }
        
        # Busca apenas os metadados
        url = f"{supabase_url}/rest/v1/{agent_table}?select=metadata"
        res = requests.get(url, headers=headers, timeout=10)
        
        if res.status_code == 200:
            data = res.json()
            unique_files = set()
            for row in data:
                metadata = row.get("metadata", {})
                if isinstance(metadata, dict):
                    filename = metadata.get("file")
                    if filename:
                        unique_files.add(filename)
            
            return jsonify({"files": sorted(list(unique_files))}), 200
        else:
            # Pode ser que a tabela não exista ainda
            if res.status_code == 404 or "does not exist" in res.text:
                return jsonify({"files": []}), 200
            return jsonify({"erro": f"Erro do Supabase: {res.text}"}), 500

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
