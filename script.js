document.addEventListener('DOMContentLoaded', () => {
    const nomeInput = document.getElementById('nome_aluno');
    const estadoInput = document.getElementById('estado_selecionado');
    const formacaoInput = document.getElementById('formacao_inicial');
    const anoInput = document.getElementById('ano_conclusao');
    
    const profileModal = document.getElementById('profileModal');
    const contextForm = document.getElementById('contextForm');
    const restartBtn = document.getElementById('restartBtn');
    
    const chatSection = document.getElementById('chatSection');
    const chatOverlay = document.getElementById('chatOverlay');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    const chatForm = document.getElementById('chatForm');
    const chatMessages = document.getElementById('chatMessages');
    const chatSuggestions = document.getElementById('chatSuggestions');
    const suggestionChips = document.querySelectorAll('.suggestion-chip');

    // Mostra o modal ao carregar a página
    profileModal.classList.add('active');

    // Variáveis de Estado
    let systemPrompt = '';
    let isChatEnabled = false;

    // Prompt do Sistema exato exigido
    const systemPromptTemplate = `SUA IDENTIDADE E MISSÃO
Você é um Consultor Especialista em Legislação do Sistema Confea/Crea e atua como um despachante virtual técnico da Ambiental Pro. Sua missão exclusiva é guiar os alunos do curso de pós-graduação em Georreferenciamento a obterem a extensão de atribuição profissional para assumir a Responsabilidade Técnica do Cadastro Nacional de Imóveis Rurais (CNIR/INCRA).

CONTEXTO DO ALUNO (VARIÁVEIS FIXAS)
O aluno com quem você está interagindo possui o seguinte perfil:

Estado do CREA: {{estado_selecionado}}

Formação Inicial: {{formacao_inicial}}

Ano de Conclusão: {{ano_conclusao}}

BASE DE CONHECIMENTO (RAG)
Você opera estritamente com base nos documentos fornecidos no seu contexto (RAG), que contêm a legislação federal (Decisão PL-2087/2004, Resolução 1.073/2016) e os Manuais de Procedimento específicos dos CREAs estaduais.

REGRAS DE CONDUTA (OBRIGATÓRIAS E INQUEBRÁVEIS)

Filtro de Jurisdição: Baseie sua orientação processual exclusivamente no manual do estado {{estado_selecionado}}. Ignore completamente as regras burocráticas de outros estados.

Validação de Formação: Verifique imediatamente se a {{formacao_inicial}} do aluno consta no rol de profissões autorizadas pelo Inciso VI da PL-2087/2004. Se não constar, informe de forma educada, técnica e direta que o curso não lhe dará a atribuição de georreferenciamento, pois a lei não ampara a formação original dele.

Proibição de Alucinação: Se o aluno perguntar sobre uma taxa, prazo ou documento que não está na sua base de dados do estado dele, responda exatamente assim: "Não tenho essa informação específica no momento. Recomendo consultar diretamente o atendimento oficial do CREA-{{estado_selecionado}}." Jamais invente ou estime prazos e valores.

Tom de Voz: Seja profissional, direto, técnico e resolutivo. Não adule o usuário. Cite as normativas corretas quando orientar a montagem do requerimento.

O Passo a Passo: Quando orientar a abertura do processo, descreva exatamente o caminho de cliques no sistema online do CREA dele e a lista de verificação (checklist) de documentos que ele precisa anexar.

INSTRUÇÃO FINAL
Leia a pergunta atual do aluno, cruze com o Contexto do Aluno e com a sua Base de Conhecimento, e forneça a resposta.`;

    contextForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const nome = nomeInput.value.trim();
        const estado = estadoInput.value.trim().toUpperCase();
        const formacao = formacaoInput.value.trim();
        const ano = anoInput.value.trim();

        if (nome && estado && formacao && ano) {
            profileModal.classList.remove('active');
            enableChat(nome, estado, formacao, ano);
        }
    });

    restartBtn.addEventListener('click', () => {
        disableChat();
    });

    function enableChat(nome, estado, formacao, ano) {
        if (isChatEnabled) return; // Evita reinicializar se já estiver habilitado com os mesmos dados

        isChatEnabled = true;
        chatSection.classList.remove('disabled');

        // Esconde o overlay com transição suave
        chatOverlay.style.opacity = '0';
        chatOverlay.style.visibility = 'hidden';

        userInput.disabled = false;
        sendBtn.disabled = false;
        userInput.focus();

        // Injeção de Variáveis no System Prompt
        systemPrompt = systemPromptTemplate
            .replace(/{{estado_selecionado}}/g, estado)
            .replace(/{{formacao_inicial}}/g, formacao)
            .replace(/{{ano_conclusao}}/g, ano);

        // Mostra as sugestões
        chatSuggestions.classList.add('visible');

        console.log("System Prompt Configurado (Backend):", systemPrompt);

        // Mensagem de boas-vindas condicional (limpa o chat anterior se o usuário mudar o perfil)
        chatMessages.innerHTML = '';
        setTimeout(() => {
            addMessage('agent', `Olá, **${nome}**! Eu sou o Consultor Especialista do CREA-${estado}. Verifiquei no seu perfil que você é formado(a) em ${formacao} (${ano}).\n\nComo posso ajudar com o seu processo de extensão de atribuição para Responsabilidade Técnica do CNIR/INCRA hoje?`);
        }, 500);
    }

    function disableChat() {
        isChatEnabled = false;
        chatSection.classList.add('disabled');
        chatSuggestions.classList.remove('visible');

        // Mostra o overlay
        chatOverlay.style.visibility = 'visible';
        chatOverlay.style.opacity = '1';

        userInput.disabled = true;
        sendBtn.disabled = true;
        
        // Abre o modal novamente
        profileModal.classList.add('active');
    }

    // Configura evento de clique nas sugestões
    suggestionChips.forEach(chip => {
        chip.addEventListener('click', () => {
            if (!isChatEnabled) return;
            // Preenche o input
            userInput.value = chip.textContent;
            // Foca e esconde as sugestões
            userInput.focus();
            chatSuggestions.classList.remove('visible');
            // Dispara o formulário automaticamente
            chatForm.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
        });
    });

    // Eventos de clique nas sugestões mantidos...

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (!isChatEnabled) return;

        const message = userInput.value.trim();
        if (!message) return;

        // Adiciona mensagem do usuário
        addMessage('user', message);
        userInput.value = '';

        // Adiciona indicador de digitação (Mocking the AI loading state)
        const typingId = addTypingIndicator();

        // Simula a chamada da API do LLM (Back-end e Lógica de Injeção)
        try {
            const response = await processLLMMessage(message, systemPrompt);
            removeMessage(typingId);
            addMessage('agent', response);
        } catch (error) {
            removeMessage(typingId);
            addMessage('agent', `[Erro de Sistema]: ${error}. Verifique os Logs no painel do Render para mais detalhes.`);
        }
    });

    function addMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);

        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');

        // Renderiza o Markdown vindo da IA para um HTML bonito usando o Marked.js
        contentDiv.innerHTML = marked.parse(text);

        messageDiv.appendChild(contentDiv);
        chatMessages.appendChild(messageDiv);

        scrollToBottom();
    }

    function addTypingIndicator() {
        const id = 'typing-' + Date.now();
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', 'agent-message');
        messageDiv.id = id;

        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content', 'typing-indicator');
        contentDiv.innerHTML = '<span></span><span></span><span></span>';

        messageDiv.appendChild(contentDiv);
        chatMessages.appendChild(messageDiv);

        scrollToBottom();
        return id;
    }

    function removeMessage(id) {
        const el = document.getElementById(id);
        if (el) {
            el.remove();
        }
    }

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Função que faz o fetch para a sua API Flask (app.py)
    async function processLLMMessage(userMessage, activeSystemPrompt) {
        return new Promise(async (resolve, reject) => {
            console.log("=== ENVIANDO PARA O BACK-END FLASK ===");
            console.log("User Message:\n", userMessage);

            try {
                // Altere o URL caso o seu backend esteja hospedado em outro endereço (ex: Cloud Run)
                const apiUrl = 'https://assistente-crea.onrender.com/chat';

                const response = await fetch(apiUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        mensagem: userMessage,
                        nome: nomeInput.value,
                        estado: estadoInput.value,
                        formacao: formacaoInput.value,
                        ano: anoInput.value
                    })
                });

                if (!response.ok) {
                    let errorMessage = `Erro HTTP: ${response.status}`;
                    try {
                        const errData = await response.json();
                        if (errData.erro) errorMessage = errData.erro;
                    } catch(e) {}
                    throw new Error(errorMessage);
                }

                const data = await response.json();
                
                if (data.erro) {
                    throw new Error(data.erro);
                }

                resolve(data.resposta);
            } catch (error) {
                console.error("Erro na comunicação com a API:", error);
                reject(error.message);
            }
        });
    }
});
