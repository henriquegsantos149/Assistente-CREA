import os
import json
import subprocess

def get_crea_context(user_query=""):
    """
    Vetoriza a pergunta do usuário e busca os trechos mais relevantes
    dos documentos no Supabase (RAG) chamando o script intermediário Node.js.
    """
    if not user_query:
        return ""
        
    script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'scripts', 'vetorizador', 'query.mjs')
    
    try:
        # Chama o Node.js
        result = subprocess.run(
            ['node', script_path, user_query], 
            capture_output=True, 
            text=True, 
            encoding='utf-8'
        )
        
        if result.returncode != 0:
            print(f"[RAG ERROR] Falha no script de busca: {result.stderr}")
            return ""
            
        # Pega a última linha (que deve conter o array JSON)
        output_lines = [linha for linha in result.stdout.strip().split('\n') if linha.startswith('[') or linha.startswith('{')]
        if not output_lines:
            return ""
            
        json_str = output_lines[-1]
        data = json.loads(json_str)
        
        if isinstance(data, dict) and "error" in data:
            print(f"[RAG SUPABASE ERROR] {data['error']}")
            return ""
            
        if not data:
            return "Nenhuma norma técnica diretamente encontrada relacionada a esta pergunta exata."
            
        textos = []
        for item in data:
            arquivo = item.get('metadata', {}).get('file', 'documento_desconhecido.md')
            sim = item.get('similarity', 0)
            textos.append(f"--- TRECHO EXTRAÍDO DE: {arquivo} (Confiança/Relevância: {sim:.2f}) ---\n{item.get('content')}")
            
        contexto_final = "\n\n".join(textos)
        print(f"[RAG SUCCESS] {len(data)} trechos recuperados do Supabase.")
        return contexto_final
        
    except Exception as e:
        print(f"[RAG EXCEPTION] Erro ao buscar contexto: {e}")
        return ""
