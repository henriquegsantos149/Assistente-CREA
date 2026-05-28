import os
import requests

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

def is_supabase_configured():
    """Verifica se as chaves do Supabase estão configuradas no ambiente."""
    return bool(SUPABASE_URL and SUPABASE_KEY)

def get_headers():
    """Retorna os headers padrão de autenticação do Supabase."""
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

def criar_ou_carregar_sessao(sessao_id, agente_id, user_nome, metadata):
    """
    Cria uma nova sessão de chat ou atualiza os metadados existentes de forma flexível via JSONB.
    Retorna o dicionário da sessão criada ou None caso o Supabase não esteja configurado.
    """
    if not is_supabase_configured():
        print("[SUPABASE] Aviso: Credenciais ausentes no .env. Ignorando persistência de sessão.")
        return None
        
    url = f"{SUPABASE_URL}/rest/v1/sessoes"
    payload = {
        "agente_id": agente_id,
        "user_nome": user_nome,
        "metadata": metadata
    }
    
    try:
        if sessao_id:
            payload["id"] = sessao_id
            # POST com preference=return=representation funciona como upsert via on_conflict
            res = requests.post(f"{url}?on_conflict=id", json=payload, headers=get_headers(), timeout=10)
        else:
            res = requests.post(url, json=payload, headers=get_headers(), timeout=10)
            
        if res.status_code in [200, 201]:
            dados_retorno = res.json()
            if dados_retorno:
                return dados_retorno[0]
        else:
            print(f"[SUPABASE ERROR] Falha ao salvar sessão (Status {res.status_code}): {res.text}")
    except Exception as e:
        print(f"[SUPABASE EXCEPTION] Erro de rede ou comunicação: {e}")
        
    return None

def persistir_mensagem(sessao_id, sender, content):
    """
    Registra uma mensagem no histórico de logs vinculada à sessão do usuário.
    Retorna True se persistido com sucesso ou False caso contrário.
    """
    if not is_supabase_configured():
        return False
        
    if not sessao_id:
        print("[SUPABASE] Erro: Tentativa de persistir mensagem sem ID de sessão válido.")
        return False

    url = f"{SUPABASE_URL}/rest/v1/mensagens"
    payload = {
        "sessao_id": sessao_id,
        "sender": sender,
        "content": content
    }
    
    try:
        res = requests.post(url, json=payload, headers=get_headers(), timeout=10)
        if res.status_code in [200, 201]:
            return True
        else:
            print(f"[SUPABASE ERROR] Falha ao persistir mensagem (Status {res.status_code}): {res.text}")
    except Exception as e:
        print(f"[SUPABASE EXCEPTION] Erro ao gravar mensagem: {e}")
        
    return False
