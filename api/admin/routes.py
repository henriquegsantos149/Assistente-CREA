import csv
import io
import json
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
        config_path = Path(__file__).parent.parent.parent / "data" / "config.json"
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                return jsonify(json.load(f)), 200
        return jsonify({"models": [], "agent_configs": {}}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@admin_bp.route('/config', methods=['POST'])
def save_config():
    try:
        dados = request.json
        config_path = Path(__file__).parent.parent.parent / "data" / "config.json"
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
        return jsonify({"status": "sucesso"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
