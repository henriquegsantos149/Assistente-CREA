import os
import glob
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from PyPDF2 import PdfReader
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)
# Libera o acesso para o seu front-end na Antigravity se comunicar com esta API
CORS(app)

# O servidor vai puxar a chave da Open Router
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

# Inicializa o cliente do OpenRouter usando a SDK da OpenAI
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

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
            if caminho.endswith('.pdf'):
                print(f"Lendo PDF: {nome_arquivo}")
                leitor = PdfReader(caminho)
                texto_pdf = ""
                for pagina in leitor.pages:
                    texto_pdf += pagina.extract_text() + "\n"
                textos.append(f"--- INÍCIO DO DOCUMENTO: {nome_arquivo} ---\n{texto_pdf}\n--- FIM DO DOCUMENTO ---")
            
            elif caminho.endswith('.txt'):
                print(f"Lendo TXT: {nome_arquivo}")
                with open(caminho, 'r', encoding='utf-8') as f:
                    textos.append(f"--- INÍCIO DO DOCUMENTO: {nome_arquivo} ---\n{f.read()}\n--- FIM DO DOCUMENTO ---")
        except Exception as e:
            print(f"Erro ao ler {nome_arquivo}: {e}")
            
    conteudo_documentos_rag = "\n\n".join(textos)
    print("Leitura de documentos concluída com sucesso!")

# Executa a leitura dos documentos ao iniciar a API
carregar_arquivos_contexto()

@app.route('/chat', methods=['POST'])
def chat_crea():
    try:
        dados = request.json
        mensagem_aluno = dados.get("mensagem")
        nome = dados.get("nome")
        estado = dados.get("estado")
        formacao = dados.get("formacao")
        ano = dados.get("ano")

        system_prompt = f"""SUA IDENTIDADE E MISSÃO
Você é um Consultor Especialista em Legislação do Sistema Confea/Crea e atua como um despachante virtual técnico da Ambiental Pro. Sua missão exclusiva é guiar os alunos do curso de pós-graduação em Georreferenciamento a obterem a extensão de atribuição profissional para assumir a Responsabilidade Técnica do Cadastro Nacional de Imóveis Rurais (CNIR/INCRA).

CONTEXTO DO ALUNO (VARIÁVEIS FIXAS)
O aluno com quem você está interagindo possui o seguinte perfil:
Nome: {nome}
Estado do CREA: {estado}
Formação Inicial: {formacao}
Ano de Conclusão: {ano}

BASE DE CONHECIMENTO (RAG)
Você opera estritamente com base nos documentos fornecidos abaixo, que contêm a legislação federal e os Manuais de Procedimento específicos dos CREAs estaduais.
{conteudo_documentos_rag}

REGRAS DE CONDUTA (OBRIGATÓRIAS E INQUEBRÁVEIS)
Filtro de Jurisdição: Baseie sua orientação processual exclusivamente no manual do estado {estado}. Ignore completamente as regras burocráticas de outros estados.
Validação de Formação: Verifique imediatamente se a {formacao} do aluno consta no rol de profissões autorizadas pelo Inciso VI da PL-2087/2004. Se não constar, informe de forma educada, técnica e direta que o curso não lhe dará a atribuição de georreferenciamento, pois a lei não ampara a formação original dele.
Proibição de Alucinação: Se o aluno perguntar sobre uma taxa, prazo ou documento que não está na sua base de dados do estado dele, responda exatamente assim: "Não tenho essa informação específica no momento. Recomendo consultar diretamente o atendimento oficial do CREA-{estado}." Jamais invente ou estime prazos e valores.
Tom de Voz: Seja profissional, direto, técnico e resolutivo. Não adule o usuário. Cite as normativas corretas quando orientar a montagem do requerimento.
O Passo a Passo: Quando orientar a abertura do processo, descreva exatamente o caminho de cliques no sistema online do CREA dele e a lista de verificação (checklist) de documentos que ele precisa anexar.

INSTRUÇÃO FINAL
Leia a pergunta atual do aluno, cruze com o Contexto do Aluno e com a sua Base de Conhecimento, e forneça a resposta."""

        # Chama a API da OpenRouter usando o modelo Gratuito do Gemini 2.5 Flash
        response = client.chat.completions.create(
            model="google/gemini-2.5-flash:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": mensagem_aluno}
            ],
            # Passa o site da Ambiental Pro para os logs do OpenRouter
            extra_headers={
                "HTTP-Referer": "https://ambientalpro.com.br", 
                "X-Title": "Assistente CREA"
            }
        )

        resposta_texto = response.choices[0].message.content

        return jsonify({"resposta": resposta_texto}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))