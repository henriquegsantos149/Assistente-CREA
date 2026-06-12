document.addEventListener('DOMContentLoaded', () => {
    // ─── Referências DOM ──────────────────────────────────
    const chatMessages        = document.getElementById('chatMessages');
    const dynamicInputWrapper = document.getElementById('dynamicInputWrapper');
    const interactiveOptions  = document.getElementById('interactiveOptions');
    const chatInputContainer  = document.getElementById('chatInputContainer');
    const chatForm            = document.getElementById('chatForm');
    const userInput           = document.getElementById('userInput');
    const sendBtn             = document.getElementById('sendBtn');
    const restartBtn          = document.getElementById('restartBtn');
    const chatSuggestions     = document.getElementById('chatSuggestions');
    const suggestionChips     = document.querySelectorAll('.suggestion-chip');

    // Caminho base dos assets — centralizado para facilitar manutenção
    const BASE_ASSETS = '../../assets/';
    const AGENT_AVATAR = `${BASE_ASSETS}Bot Pro.svg`;

    // ─── Estado da Sessão ─────────────────────────────────
    let currentChatSession = 0;
    let onboardingState = 'START'; // START | NAME | DEGREE | YEAR | HAS_CREA | STATE | READY
    let sessaoId = null;
    let historicoChat = []; // [{role: "user"|"assistant", content: "..."}]

    let userData = {
        nome: '',
        formacao: '',
        ano: '',
        hasCrea: '',
        estado: ''
    };

    // ─── Inicialização ────────────────────────────────────
    startOnboarding();

    if (restartBtn) {
        restartBtn.addEventListener('click', () => startOnboarding());
    }

    // ─── Controle de Carregamento ─────────────────────────
    /**
     * Ativa ou desativa o estado de loading no botão de envio.
     * Também desabilita o input para evitar envios duplos.
     */
    function setLoading(isLoading) {
        sendBtn.disabled = isLoading;
        userInput.disabled = isLoading;
        if (isLoading) {
            sendBtn.classList.add('loading');
        } else {
            sendBtn.classList.remove('loading');
        }
    }

    // ─── Onboarding ───────────────────────────────────────
    function startOnboarding() {
        currentChatSession++;
        const session = currentChatSession;

        chatMessages.innerHTML = '';
        onboardingState = 'NAME';
        sessaoId = null;
        historicoChat = [];
        userData = { nome: '' };

        chatSuggestions.classList.remove('visible');
        hideInput();

        const welcomeParts = [
            `Oi! Seja muito bem-vindo(a). Eu sou a Secretaria Acadêmica Digital, e meu papel é facilitar a sua vida! Estou aqui para te ajudar de forma rápida com documentos, declarações, boletos e qualquer dúvida administrativa da sua jornada com a gente.`,
            `Como posso te chamar?`
        ];

        displaySequentialMessages(welcomeParts, session).then(() => {
            if (currentChatSession === session) {
                showTextInput('Digite seu nome...');
            }
        });
    }

    // ─── Controle de Input ────────────────────────────────
    function hideInput() {
        dynamicInputWrapper.style.opacity = '0';
        dynamicInputWrapper.style.pointerEvents = 'none';
        interactiveOptions.style.display = 'none';
        chatInputContainer.style.display = 'none';
        interactiveOptions.innerHTML = '';
        userInput.value = '';
        setLoading(false);
    }

    function showTextInput(placeholderText = 'Digite sua resposta...', type = 'text') {
        interactiveOptions.style.display = 'none';
        chatInputContainer.style.display = 'block';

        userInput.type = type;
        userInput.placeholder = placeholderText;
        userInput.disabled = false;
        sendBtn.disabled = false;
        sendBtn.classList.remove('loading');

        dynamicInputWrapper.style.opacity = '1';
        dynamicInputWrapper.style.pointerEvents = 'all';
        userInput.focus();
    }

    function showInteractiveOptions(options) {
        chatInputContainer.style.display = 'none';
        interactiveOptions.style.display = 'flex';
        interactiveOptions.innerHTML = '';

        options.forEach(opt => {
            const btn = document.createElement('button');
            btn.classList.add('option-btn');
            btn.textContent = opt.label;
            btn.addEventListener('click', () => handleOptionClick(opt.value, opt.label));
            interactiveOptions.appendChild(btn);
        });

        dynamicInputWrapper.style.opacity = '1';
        dynamicInputWrapper.style.pointerEvents = 'all';
    }

    function handleOptionClick(value, label) {
        processUserInput(value, label);
    }

    // ─── Submit do Formulário ─────────────────────────────
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const text = userInput.value.trim();
        if (!text) return;

        if (onboardingState === 'READY') {
            chatSuggestions.classList.remove('visible');
        }

        processUserInput(text, text);
    });

    // ─── Chips de Sugestão ────────────────────────────────
    suggestionChips.forEach(chip => {
        chip.addEventListener('click', () => {
            if (onboardingState !== 'READY') return;
            chatSuggestions.classList.remove('visible');
            userInput.value = chip.textContent;
            chatForm.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
        });
    });

    // ─── Processamento Principal ──────────────────────────
    async function processUserInput(value, displayLabel) {
        const session = currentChatSession;

        addMessage('user', displayLabel);
        hideInput();

        // ── Onboarding: NAME ──
        if (onboardingState === 'NAME') {
            const typingId = addTypingIndicator();

            // Regex local de fallback para extração do nome
            let regexName = value;
            while (true) {
                let cleaned = regexName.replace(
                    /^(eu sou o|eu sou a|eu me chamo|sou o|sou a|sou|me chamo|meu nome é|meu nome e|o meu nome é|o meu nome e|olá|ola|bom dia|boa tarde|boa noite|pode me chamar de)[\s,]+/gi,
                    ''
                ).trim();
                if (cleaned === regexName) break;
                regexName = cleaned;
            }
            let nameParts = regexName.split(' ');
            if (nameParts.length > 2) nameParts = nameParts.slice(0, 2);
            regexName = nameParts.map(w => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase()).join(' ');

            try {
                const extractedName = await extractNameViaLLM(value);
                if (currentChatSession !== session) return;
                removeMessage(typingId);
                userData.nome = extractedName || regexName || value;
            } catch {
                if (currentChatSession !== session) return;
                removeMessage(typingId);
                userData.nome = regexName || value;
            }

            onboardingState = 'READY';
            await displaySequentialMessages(
                [`Tudo certo, **${userData.nome}**! Como posso te ajudar hoje?`],
                session
            );
            if (currentChatSession === session) {
                showTextInput('Digite sua dúvida...');
                chatSuggestions.classList.add('visible');
            }
            return;
        }

        // ── READY: Chamada ao LLM ──
        if (onboardingState === 'READY') {
            const typingId = addTypingIndicator();
            setLoading(true);

            historicoChat.push({ role: 'user', content: value });

            try {
                const response = await processLLMMessage(value);
                if (currentChatSession !== session) return;
                removeMessage(typingId);
                setLoading(false);

                historicoChat.push({ role: 'assistant', content: response });
                if (historicoChat.length > 12) {
                    historicoChat = historicoChat.slice(-12);
                }

                const parts = response
                    .split('---MENSAGEM---')
                    .map(p => p.trim())
                    .filter(p => p.length > 0);

                await displaySequentialMessages(parts, session);
                if (currentChatSession === session) {
                    showTextInput('Digite sua resposta...');
                }
            } catch (error) {
                if (currentChatSession !== session) return;
                removeMessage(typingId);
                setLoading(false);

                // Remove a mensagem do usuário que falhou do histórico
                historicoChat.pop();

                addErrorMessage(error);
                showTextInput('Tente novamente...');
            }
        }
    }

    // ─── Mensagens ────────────────────────────────────────
    function addMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message-bubble', `${sender}-message`);

        const parsedText = marked.parse(text);

        if (sender === 'agent') {
            messageDiv.innerHTML = `
                <div class="agent-avatar"><img src="${AGENT_AVATAR}" alt="Agente Pro" loading="lazy"></div>
                <div class="message-content">${parsedText}</div>
            `;
        } else {
            messageDiv.innerHTML = `<div class="message-content">${parsedText}</div>`;
        }

        chatMessages.appendChild(messageDiv);
        scrollToBottom();
        return messageDiv;
    }

    /**
     * Classifica o erro e exibe uma mensagem amigável e diferenciada.
     */
    function addErrorMessage(error) {
        const errorStr = (error?.toString() || '').toLowerCase();
        let msg;

        if (errorStr.includes('failed to fetch') || errorStr.includes('networkerror') || errorStr.includes('network error')) {
            msg = '**Sem conexão:** Verifique sua internet e tente novamente.';
        } else if (errorStr.includes('timeout') || errorStr.includes('408')) {
            msg = '**Tempo esgotado:** O servidor demorou demais para responder. Tente novamente.';
        } else if (errorStr.includes('503') || errorStr.includes('502') || errorStr.includes('unavailable')) {
            msg = '**Serviço indisponível:** O servidor está temporariamente fora do ar. Aguarde um momento.';
        } else if (errorStr.includes('401') || errorStr.includes('403')) {
            msg = '**Erro de autenticação:** Chave da API inválida ou expirada. Contate o suporte.';
        } else {
            msg = `**Erro de comunicação:** ${error || 'Tente novamente em instantes.'}`;
        }

        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message-bubble', 'agent-message', 'error-bubble');
        messageDiv.innerHTML = `
            <div class="agent-avatar"><img src="${AGENT_AVATAR}" alt="Agente Pro" loading="lazy"></div>
            <div class="message-content">${marked.parse(msg)}</div>
        `;
        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }

    async function displaySequentialMessages(parts, session) {
        for (let i = 0; i < parts.length; i++) {
            if (currentChatSession !== session) return;

            const chars = parts[i].length;
            const delay = Math.min(2500, Math.max(800, chars * 12));

            const typingId = addTypingIndicator();
            await sleep(delay);

            if (currentChatSession !== session) return;

            removeMessage(typingId);

            const msgContainer = document.createElement('div');
            msgContainer.classList.add('message-bubble', 'agent-message');
            msgContainer.innerHTML = `
                <div class="agent-avatar"><img src="${AGENT_AVATAR}" alt="Agente Pro" loading="lazy"></div>
                <div class="message-content">${marked.parse(parts[i])}</div>
            `;
            chatMessages.appendChild(msgContainer);
            scrollToBottom();

            if (i < parts.length - 1) {
                await sleep(400);
            }
        }
    }

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    function addTypingIndicator() {
        const id = 'typing-' + Date.now();
        chatMessages.insertAdjacentHTML('beforeend', `
            <div class="message-bubble agent-message" id="${id}">
                <div class="agent-avatar"><img src="${AGENT_AVATAR}" alt="Agente Pro" loading="lazy"></div>
                <div class="typing-indicator">
                    <span></span><span></span><span></span>
                </div>
            </div>
        `);
        scrollToBottom();
        return id;
    }

    function removeMessage(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function scrollToBottom() {
        setTimeout(() => {
            chatMessages.scrollTo({ top: chatMessages.scrollHeight, behavior: 'smooth' });
        }, 80);
    }

    // ─── Comunicação com o Backend ────────────────────────
    async function processLLMMessage(userMessage) {
        const response = await fetch('/api/secretaria/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                mensagem:  userMessage,
                nome:      userData.nome,
                estado:    userData.estado,
                formacao:  userData.formacao,
                ano:       userData.ano,
                hasCrea:   userData.hasCrea,
                sessao_id: sessaoId,
                historico: historicoChat
            })
        });

        if (!response.ok) {
            let errorMessage = `Erro HTTP: ${response.status}`;
            try {
                const errData = await response.json();
                if (errData.erro) errorMessage = errData.erro;
            } catch (_) {}
            throw new Error(errorMessage);
        }

        const data = await response.json();

        if (data.erro) throw new Error(data.erro);
        if (data.sessao_id) sessaoId = data.sessao_id;

        return data.resposta;
    }

    async function extractNameViaLLM(userMessage) {
        const response = await fetch('/api/secretaria/extract-name', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mensagem: userMessage })
        });

        if (!response.ok) throw new Error(`Erro HTTP: ${response.status}`);

        const data = await response.json();
        if (data.erro) throw new Error(data.erro);

        return data.nome;
    }
});
