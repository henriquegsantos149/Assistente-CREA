import os
import glob
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)
# Libera o acesso para o seu front-end na Antigravity se comunicar com esta API
CORS(app)

# O servidor vai puxar a chave secreta do cofre do Google, nunca do código fonte
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Faz o upload dos documentos de contexto para o Gemini
arquivos_rag = []

def carregar_arquivos_contexto():
    global arquivos_rag
    # Evita rodar se a chave não estiver configurada ainda
    if not GEMINI_API_KEY:
        return
        
    pasta = os.path.join(os.path.dirname(__file__), 'Documentos')
    if not os.path.exists(pasta):
        return
        
    for nome_arquivo in os.listdir(pasta):
        caminho = os.path.join(pasta, nome_arquivo)
        if caminho.endswith('.pdf') or caminho.endswith('.txt'):
            try:
                print(f"Fazendo upload para a IA do documento: {nome_arquivo}")
                arquivo_enviado = genai.upload_file(caminho)
                arquivos_rag.append(arquivo_enviado)
            except Exception as e:
                print(f"Erro ao enviar {nome_arquivo}: {e}")

# Executa o carregamento dos documentos ao iniciar a API
carregar_arquivos_contexto()

@app.route('/chat', methods=['POST'])
def chat_crea():
    try:
        dados = request.json
        mensagem_aluno = dados.get("mensagem")
        estado = dados.get("estado")
        formacao = dados.get("formacao")
        ano = dados.get("ano")

        system_prompt = f"""SUA IDENTIDADE E MISSÃO
Você é um Consultor Especialista em Legislação do Sistema Confea/Crea e atua como um despachante virtual técnico da Ambiental Pro. Sua missão exclusiva é guiar os alunos do curso de pós-graduação em Georreferenciamento a obterem a extensão de atribuição profissional para assumir a Responsabilidade Técnica do Cadastro Nacional de Imóveis Rurais (CNIR/INCRA).

CONTEXTO DO ALUNO (VARIÁVEIS FIXAS)
O aluno com quem você está interagindo possui o seguinte perfil:
Estado do CREA: {estado}
Formação Inicial: {formacao}
Ano de Conclusão: {ano}

BASE DE CONHECIMENTO (RAG)
Você opera estritamente com base nos documentos fornecidos no seu contexto (RAG), que contêm a legislação federal (Decisão PL-2087/2004, Resolução 1.073/2016) e os Manuais de Procedimento específicos dos CREAs estaduais.

REGRAS DE CONDUTA (OBRIGATÓRIAS E INQUEBRÁVEIS)
Filtro de Jurisdição: Baseie sua orientação processual exclusivamente no manual do estado {estado}. Ignore completamente as regras burocráticas de outros estados.
Validação de Formação: Verifique imediatamente se a {formacao} do aluno consta no rol de profissões autorizadas pelo Inciso VI da PL-2087/2004. Se não constar, informe de forma educada, técnica e direta que o curso não lhe dará a atribuição de georreferenciamento, pois a lei não ampara a formação original dele.
Proibição de Alucinação: Se o aluno perguntar sobre uma taxa, prazo ou documento que não está na sua base de dados do estado dele, responda exatamente assim: "Não tenho essa informação específica no momento. Recomendo consultar diretamente o atendimento oficial do CREA-{estado}." Jamais invente ou estime prazos e valores.
Tom de Voz: Seja profissional, direto, técnico e resolutivo. Não adule o usuário. Cite as normativas corretas quando orientar a montagem do requerimento.
O Passo a Passo: Quando orientar a abertura do processo, descreva exatamente o caminho de cliques no sistema online do CREA dele e a lista de verificação (checklist) de documentos que ele precisa anexar.

INSTRUÇÃO FINAL
Leia a pergunta atual do aluno, cruze com o Contexto do Aluno e com a sua Base de Conhecimento, e forneça a resposta."""

        # Configuração do Modelo e do RAG (Prompt do Sistema)
        # Atenção: gemini-1.5-flash é mais estável na versão gratuita e atende perfeitamente os PDFs
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_prompt
        )

        # Junta a mensagem do aluno com os arquivos PDF carregados
        conteudo_prompt = arquivos_rag + [mensagem_aluno]

        # Envia a mensagem para o Google
        resposta = model.generate_content(conteudo_prompt)

        # Devolve a resposta formatada para a página do aluno
        return jsonify({"resposta": resposta.text}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))