import os
import logging
import requests

logger = logging.getLogger(__name__)

import json
from pathlib import Path

logger = logging.getLogger(__name__)

def get_modelos_fallback():
    try:
        config_path = Path(__file__).parent.parent.parent / "data" / "config.json"
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                return config.get("models", [
                    "meta-llama/llama-3.3-70b-instruct:free",
                    "google/gemma-3-27b-it:free"
                ])
    except Exception as e:
        logger.error(f"Erro ao carregar config.json: {e}")
        
    return [
        "meta-llama/llama-3.3-70b-instruct:free",
        "google/gemma-3-27b-it:free",
        "google/gemma-3-12b-it:free",
        "mistralai/mistral-7b-instruct:free",
    ]


def call_openrouter(system_prompt, user_message, history=None, max_tokens=None, temperature=0.1):
    """
    Chama a API OpenRouter com sistema de fallback entre modelos.

    Args:
        system_prompt: Instrução de sistema para o modelo.
        user_message: Mensagem atual do usuário.
        history: Lista de mensagens anteriores [{"role": "user"|"assistant", "content": "..."}].
        max_tokens: Limite máximo de tokens na resposta (None = sem limite).
        temperature: Temperatura de geração (0.0–1.0).

    Returns:
        String com o conteúdo da resposta do modelo.

    Raises:
        Exception: Se todos os modelos falharem.
    """
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise Exception("OPENROUTER_API_KEY não configurada no ambiente.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://ambientalpro.com.br",
        "X-Title": "Assistente IA - Ambiental Pro",
    }

    ultimo_erro = None
    modelos = get_modelos_fallback()
    
    for modelo in modelos:
        try:
            payload_messages = [{"role": "system", "content": system_prompt}]
            if history:
                payload_messages.extend(history)
            payload_messages.append({"role": "user", "content": user_message})

            payload = {
                "model": modelo,
                "messages": payload_messages,
                "temperature": temperature,
            }
            if max_tokens:
                payload["max_tokens"] = max_tokens

            res = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=int(os.environ.get("LLM_TIMEOUT_SECONDS", 60)),
            )
            data = res.json()

            if "error" in data:
                codigo_erro = data["error"].get("code", "?")
                ultimo_erro = f"Modelo '{modelo}' falhou com código {codigo_erro}."
                logger.warning("[LLM FALLBACK] %s Tentando próximo...", ultimo_erro)
                continue

            if "choices" not in data or not data["choices"]:
                ultimo_erro = f"Modelo '{modelo}' retornou resposta vazia."
                logger.warning("[LLM FALLBACK] %s Tentando próximo...", ultimo_erro)
                continue

            logger.info("[LLM OK] Resposta obtida com modelo: %s", modelo)
            return data["choices"][0]["message"]["content"]

        except requests.exceptions.Timeout:
            ultimo_erro = f"Timeout ao chamar '{modelo}'."
            logger.warning("[LLM FALLBACK] %s Tentando próximo...", ultimo_erro)
        except Exception as exc:
            ultimo_erro = f"Exceção ao chamar '{modelo}': {exc}"
            logger.warning("[LLM FALLBACK] %s Tentando próximo...", ultimo_erro)

    raise Exception(f"Todos os modelos falharam. Último erro: {ultimo_erro}")
