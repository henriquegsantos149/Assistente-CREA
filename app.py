import os
import glob
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import requests
import json
import re

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# Libera o acesso restrito aos domínios permitidos (para segurança da API Key)
origens_permitidas = [
    "http://localhost:5000",
    "http://localhost:8080",
    "http://127.0.0.1:5000",
    "http://127.0.0.1:8080",
    "https://ambientalpro.com.br",
    "https://www.ambientalpro.com.br",
    re.compile(r"https://.*\.vercel\.app$")
]
CORS(app, resources={r"/*": {"origins": origens_permitidas}})

# O servidor vai puxar a chave da Open Router
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

# Faz a extração do texto dos documentos de contexto
conteudo_documentos_rag = ""

def carregar_arquivos_contexto():
    global conteudo_documentos_rag
    pasta = os.path.join(os.path.dirname(__file__), 'Documentos')
    if not os.path.exists(pasta):
        print("Pasta Documentos não encontrada.")
        return
        
    textos = []
    for nome_arquivo in os.listdir(pasta):
        caminho = os.path.join(pasta, nome_arquivo)
        try:
            if caminho.endswith('.md') or caminho.endswith('.txt'):
                print(f"Lendo documento de texto: {nome_arquivo}")
                with open(caminho, 'r', encoding='utf-8') as f:
                    textos.append(f"--- INÍCIO DO DOCUMENTO: {nome_arquivo} ---\n{f.read()}\n--- FIM DO DOCUMENTO ---")
        except Exception as e:
            print(f"Erro ao ler {nome_arquivo}: {e}")
            
    conteudo_documentos_rag = "\n\n".join(textos)
    print("Leitura de documentos Markdown/TXT concluída com sucesso!")

# Executa a leitura dos documentos ao iniciar a API
carregar_arquivos_contexto()

@app.route('/extract-name', methods=['POST'])
def extract_name():
    try:
        dados = request.json
        mensagem_aluno = dados.get("mensagem", "")

        system_prompt = "Sua única função é extrair o NOME do usuário a partir da frase fornecida. Responda APENAS com o nome extraído, com a primeira letra maiúscula. Exemplo: se o usuário disser 'Olá, me chamo João Pedro', responda APENAS 'João Pedro'. Se disser 'sou o marcos', responda 'Marcos'. Não escreva mais nenhuma palavra."

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://ambientalpro.com.br",
            "X-Title": "Assistente CREA"
        }

        MODELOS_FALLBACK = [
            "meta-llama/llama-3.3-70b-instruct:free",
            "google/gemma-4-31b-it:free",
            "google/gemma-4-26b-a4b-it:free"
        ]

        resposta_texto = None
        for modelo in MODELOS_FALLBACK:
            try:
                payload = {
                    "model": modelo,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": mensagem_aluno}
                    ],
                    "temperature": 0.1
                }
                res = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers, timeout=15)
                data = res.json()
                if "error" not in data and "choices" in data and data["choices"]:
                    resposta_texto = data["choices"][0]["message"]["content"].strip()
                    # Remove pontuações finais residuais, caso a IA coloque
                    resposta_texto = resposta_texto.replace(".", "").replace("!", "").strip()
                    break
            except:
                continue

        if not resposta_texto or len(resposta_texto.split()) > 3 or "meu nome" in resposta_texto.lower() or "me chamo" in resposta_texto.lower():
            # Fallback robusto usando Regex caso a IA falhe (Rate limit ou alucinação)
            limpo = re.sub(r"^(eu sou o|eu sou a|sou o|sou a|sou|me chamo|meu nome [eé]|ol[aá]|bom dia|boa tarde|boa noite|pode me chamar de)[\s,]*", "", mensagem_aluno, flags=re.IGNORECASE).strip()
            # Pega até os 2 primeiros nomes
            palavras = limpo.split()
            if palavras:
                resposta_texto = " ".join([p.capitalize() for p in palavras[:2]])
            else:
                resposta_texto = mensagem_aluno

        return jsonify({"nome": resposta_texto}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat_crea():
    try:
        dados = request.json
        mensagem_aluno = dados.get("mensagem")
        nome = dados.get("nome", "Aluno")
        estado = dados.get("estado", "Desconhecido")
        formacao = dados.get("formacao", "Desconhecida")
        ano = dados.get("ano", "Desconhecido")
        has_crea = dados.get("hasCrea", "Não informado")

        system_prompt = f"""Você é o Agente Pro, um agente conversacional com IA operando 24 horas por dia da Ambiental Pro. Você escreve SEMPRE em português do Brasil correto e formal, sem NENHUM erro ortográfico, gramatical ou de vocabulário.

═══════════════════════════════════════════════════════
PERFIL DO ALUNO ATENDIDO:
- Nome: {nome}
- Formação Inicial: {formacao} (concluída em {ano})
- Já possui registro no CREA ativo? {has_crea}
- CREA de atuação que busca a atribuição: {estado}
═══════════════════════════════════════════════════════

SUA BASE DE CONHECIMENTO OFICIAL:
Os documentos abaixo contêm a legislação federal, o glossário de terminologia oficial e os manuais dos Conselhos Regionais. Você SÓ pode afirmar algo se encontrar respaldo explícito neles.
{conteudo_documentos_rag}

DADOS DA INSTITUIÇÃO AMBIENTAL PRO:
Sempre que necessário, informe que a faculdade parceira é o Centro Universitário Anhanguera Pitágoras (UNOPAR DE NITERÓI - UNIAN), com Decisão Plenária PL/RJ n.º 00307/2025 (CREA-RJ).

═══════════════════════════════════════════════════════
REGRAS ABSOLUTAS — ANTI-ALUCINAÇÃO (NUNCA VIOLE)
═══════════════════════════════════════════════════════

REGRA 1 — IDIOMA E TOM:
- Escreva exclusivamente em português.
- Seja profissional, empático e engajador. Chame o aluno pelo nome ({nome}).

REGRA 2 — TERMINOLOGIA OFICIAL OBRIGATÓRIA:
Use APENAS os termos do GLOSSÁRIO_TERMOS_OFICIAIS_CREA.md carregado na sua base. NUNCA invente termos como "discharge" ou "voucher".

REGRA 3 — DADOS SEM FONTE:
Se um dado NÃO estiver explicitamente nos documentos da base, diga: "Não tenho esse dado na minha base. Consulte diretamente o site oficial do CREA-{estado}". Nunca invente prazos ou taxas.

REGRA 4 — REGRA DE JURISDIÇÃO:
Baseie sua orientação processual EXCLUSIVAMENTE no manual do estado {estado}. Ignore procedimentos de outros estados.
Se o estado do aluno NÃO FOR o Rio de Janeiro (RJ), alerte que "O CREA-{estado} realizará uma consulta inter-regional (visto/diligência) ao CREA-RJ, onde a Pós-graduação está registrada."

REGRA 5 — ELEGIBILIDADE DA FORMAÇÃO:
Verifique se a formação "{formacao}" está listada no Inciso VI da PL-2087/2004. Atenção redobrada: A graduação em Geografia COM a pós-graduação é TOTALMENTE ELEGÍVEL para assinar laudos do INCRA. NUNCA afirme que o Geógrafo não pode assinar ou que precisa de diploma de Engenharia.

REGRA 6 — REGISTRO ATIVO:
O aluno declarou que: "{has_crea}" possui registro ativo. Se ele disser que "Não", explique que a extensão da Pós só pode ser solicitada caso ele já possua um registro principal no CREA.

REGRA 7 — CONCISÃO EXTREMA E OBJETIVIDADE:
Nunca cite textos inteiros de leis, não dê "aulas teóricas", não use jargões difíceis desnecessários. Vá direto ao ponto. Respostas longas são proibidas.

═══════════════════════════════════════════════════════
COMO VOCÊ SE COMUNICA (ESTILO WHATSAPP)
═══════════════════════════════════════════════════════

Você DEVE separar sua resposta em 2 a 4 "balões" curtos usando EXATAMENTE o delimitador `---MENSAGEM---` em uma linha isolada. NUNCA mande um bloco único de texto.

ESTRUTURA OBRIGATÓRIA DA RESPOSTA:
1. Balão 1: Veredito direto, celebrando caso ele tenha a formação + a pós da Ambiental Pro.
---MENSAGEM---
2. Balão 2: Resumo do que ele precisa fazer (Passos principais curtos).
---MENSAGEM---
3. Balão 3: Uma pergunta de engajamento amigável (Ex: "Quer ajuda com a documentação?").

Exemplo de formato correto:
Boas notícias, {nome}! Com a sua graduação em Geografia e a Pós da Ambiental Pro (homologada no CREA-RJ), você tem total direito à atribuição de georreferenciamento! 🚀

---MENSAGEM---

Para dar entrada no CREA-{estado}, você só precisa anexar seu diploma e histórico da pós no sistema SITAC.

---MENSAGEM---

Quer que eu te mostre o passo a passo de como abrir esse protocolo no site? NUNCA DEIXE DE USAR O DELIMITADOR ENTRE AS MENSAGENS."""

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://ambientalpro.com.br",
            "X-Title": "Assistente CREA"
        }

        # Lista de modelos verificados e ativos na OpenRouter (atualizada em Mai/2026)
        MODELOS_FALLBACK = [
            "meta-llama/llama-3.3-70b-instruct:free",   # 1º - O mais inteligente
            "google/gemma-4-31b-it:free",               # 2º - Gemma 4 do Google
            "google/gemma-4-26b-a4b-it:free",           # 3º - Variante eficiente do Gemma 4
            "nvidia/nemotron-nano-12b-v2-vl:free",      # 4º - Nemotron da Nvidia (estável)
        ]

        resposta_texto = None
        ultimo_erro = None

        for modelo in MODELOS_FALLBACK:
            try:
                payload = {
                    "model": modelo,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": mensagem_aluno}
                    ]
                }

                res = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    json=payload,
                    headers=headers,
                    timeout=60
                )
                data = res.json()

                # Se a API retornou um erro (429, 404, etc.), tenta o próximo modelo
                if "error" in data:
                    codigo_erro = data["error"].get("code", "?")
                    ultimo_erro = f"Modelo '{modelo}' falhou com código {codigo_erro}."
                    print(f"[FALLBACK] {ultimo_erro} Tentando próximo...")
                    continue

                if "choices" not in data or not data["choices"]:
                    ultimo_erro = f"Modelo '{modelo}' retornou resposta vazia."
                    print(f"[FALLBACK] {ultimo_erro} Tentando próximo...")
                    continue

                # Resposta válida encontrada!
                resposta_texto = data["choices"][0]["message"]["content"]
                print(f"[OK] Resposta obtida com sucesso usando o modelo: {modelo}")
                break

            except Exception as e:
                ultimo_erro = f"Exceção ao chamar '{modelo}': {str(e)}"
                print(f"[FALLBACK] {ultimo_erro} Tentando próximo...")
                continue

        if resposta_texto is None:
            raise Exception(f"Todos os modelos falharam. Último erro: {ultimo_erro}")

        return jsonify({"resposta": resposta_texto}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))