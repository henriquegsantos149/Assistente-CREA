document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chatMessages');
    const dynamicInputWrapper = document.getElementById('dynamicInputWrapper');
    const interactiveOptions = document.getElementById('interactiveOptions');
    const chatInputContainer = document.getElementById('chatInputContainer');
    const chatForm = document.getElementById('chatForm');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    const restartBtn = document.getElementById('restartBtn');
    const chatSuggestions = document.getElementById('chatSuggestions');
    const suggestionChips = document.querySelectorAll('.suggestion-chip');

    // Variáveis de Estado
    let currentChatSession = 0; 
    let onboardingState = 'START'; // START, NAME, DEGREE, YEAR, HAS_CREA, STATE, READY
    
    let userData = {
        nome: '',
        formacao: '',
        ano: '',
        hasCrea: '',
        estado: ''
    };

    // Inicia o chat automaticamente ao carregar
    startOnboarding();

    if (restartBtn) {
        restartBtn.addEventListener('click', () => {
            startOnboarding();
        });
    }

    function startOnboarding() {
        currentChatSession++;
        const session = currentChatSession;
        
        chatMessages.innerHTML = '';
        onboardingState = 'NAME';
        userData = { nome: '', formacao: '', ano: '', hasCrea: '', estado: '' };
        
        chatSuggestions.classList.remove('visible');
        hideInput();

        const welcomeParts = [
            `Olá, seja muito bem-vindo(a)! Eu sou o Agente Pro, um agente conversacional com IA que opera 24 horas por dia, todos os dias, para te auxiliar em sua carreira profissional.`,
            `Para começar, gostaria de saber o seu nome.`
        ];
        
        displaySequentialMessages(welcomeParts, session).then(() => {
            if (currentChatSession === session) {
                showTextInput('Digite seu nome...');
            }
        });
    }

    function hideInput() {
        dynamicInputWrapper.style.opacity = '0';
        dynamicInputWrapper.style.pointerEvents = 'none';
        
        // Hide specific elements
        interactiveOptions.style.display = 'none';
        chatInputContainer.style.display = 'none';
        interactiveOptions.innerHTML = '';
        userInput.value = '';
    }

    function showTextInput(placeholderText = 'Digite sua resposta...', type = 'text') {
        interactiveOptions.style.display = 'none';
        chatInputContainer.style.display = 'block';
        
        userInput.type = type;
        userInput.placeholder = placeholderText;
        userInput.disabled = false;
        sendBtn.disabled = false;
        
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
        // Mock user submitting this text
        userInput.value = value;
        
        // Process submission
        processUserInput(value, label);
    }

        chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const text = userInput.value.trim();
        if (!text) return;
        
        // Esconde as sugestões assim que o usuário digita algo na fase final
        if (onboardingState === 'READY') {
            chatSuggestions.classList.remove('visible');
        }

        processUserInput(text, text);
    });

    suggestionChips.forEach(chip => {
        chip.addEventListener('click', () => {
            if (onboardingState !== 'READY') return;
            chatSuggestions.classList.remove('visible');
            userInput.value = chip.textContent;
            chatForm.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
        });
    });

    async function processUserInput(value, displayLabel) {
        const session = currentChatSession;
        
        // Adiciona a mensagem do usuário na tela
        addMessage('user', displayLabel);
        hideInput();

        // Lógica da Máquina de Estados (Onboarding)
        if (onboardingState === 'NAME') {
            const typingId = addTypingIndicator();
            
            // Regex local rápida (fallback)
            let regexName = value.replace(/^(eu sou o|eu sou a|sou o|sou a|sou|me chamo|meu nome é|meu nome e|olá|ola|bom dia|boa tarde|boa noite|pode me chamar de)[\s,]+/gi, '').trim();
            // Capitaliza as palavras
            regexName = regexName.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase()).join(' ');

            try {
                // Chama a API para extrair apenas o nome da frase
                const extractedName = await extractNameViaLLM(value);
                if (currentChatSession !== session) return;
                removeMessage(typingId);
                
                // Se a IA falhar e voltar vazio, usamos o valor do regex
                userData.nome = extractedName || regexName || value;
            } catch (e) {
                if (currentChatSession !== session) return;
                removeMessage(typingId);
                userData.nome = regexName || value; // Fallback se a API der erro 404
            }
            
            onboardingState = 'DEGREE';
            await displaySequentialMessages([`Muito prazer, **${userData.nome}**! Qual é a sua formação inicial (graduação)?`], session);
            if (currentChatSession === session) showTextInput('Ex: Engenharia Ambiental');
            return;
        }

        if (onboardingState === 'DEGREE') {
            userData.formacao = value;
            onboardingState = 'YEAR';
            await displaySequentialMessages([`Legal! E em que ano você concluiu essa sua graduação?`], session);
            if (currentChatSession === session) showTextInput('Ex: 2015', 'number');
            return;
        }

        if (onboardingState === 'YEAR') {
            userData.ano = value;
            onboardingState = 'HAS_CREA';
            await displaySequentialMessages([`Você já possui registro ativo no CREA?`], session);
            if (currentChatSession === session) {
                showInteractiveOptions([
                    { label: 'Sim', value: 'Sim' },
                    { label: 'Não', value: 'Não' }
                ]);
            }
            return;
        }

        if (onboardingState === 'HAS_CREA') {
            userData.hasCrea = value;
            onboardingState = 'STATE';
            await displaySequentialMessages([`Perfeito. Para finalizarmos o seu perfil, em qual estado (sigla) você busca a extensão de atribuição?`], session);
            if (currentChatSession === session) showTextInput('Ex: SP, RJ, MG...');
            return;
        }

        if (onboardingState === 'STATE') {
            userData.estado = value.toUpperCase();
            onboardingState = 'READY';
            
            // Inicia o atendimento da IA
            await displaySequentialMessages([`Tudo certo! Como posso te ajudar com o seu processo hoje?`], session);
            if (currentChatSession === session) {
                showTextInput('Digite sua dúvida...');
                chatSuggestions.classList.add('visible'); // Mostra as sugestões ao concluir o onboarding
            }
            return;
        }

        if (onboardingState === 'READY') {
            // Fase da IA: Repassa para o backend
            const typingId = addTypingIndicator();
            try {
                const response = await processLLMMessage(value);
                if (currentChatSession !== session) return; 
                removeMessage(typingId);

                // Divide a resposta pelo delimitador ---MENSAGEM---
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
                addMessage('agent', `**Erro de comunicação:** ${error}.`);
                showTextInput('Tente novamente...');
            }
        }
    }

    function addMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message-bubble', `${sender}-message`);

        const parsedText = marked.parse(text);

        if (sender === 'agent') {
            messageDiv.innerHTML = `
                <div class="agent-avatar"><img src="assets/Bot Pro.png" alt="Agent"></div>
                <div class="message-content">${parsedText}</div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="message-content">${parsedText}</div>
            `;
        }

        chatMessages.appendChild(messageDiv);
        scrollToBottom();
        return messageDiv;
    }

    // Exibe um array de mensagens sequencialmente, com delay e typing indicator entre elas
    async function displaySequentialMessages(parts, session) {
        for (let i = 0; i < parts.length; i++) {
            if (currentChatSession !== session) return; 

            const chars = parts[i].length;
            const delay = Math.min(2500, Math.max(800, chars * 12));

            const typingId = addTypingIndicator();
            await sleep(delay);
            
            if (currentChatSession !== session) return; 
            
            removeMessage(typingId);
            
            // Cria o elemento da mensagem com o avatar personalizado
            const msgContainer = document.createElement('div');
            msgContainer.classList.add('message-bubble', 'agent-message');
            msgContainer.innerHTML = `
                <div class="agent-avatar"><img src="assets/Bot Pro.png" alt="Agent"></div>
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

    // Utilitário para adicionar o indicador de digitação da IA
    function addTypingIndicator() {
        const id = 'typing-' + Date.now();
        const typingHTML = `
            <div class="message-bubble agent-message" id="${id}">
                <div class="agent-avatar"><img src="assets/Bot Pro.png" alt="Agent"></div>
                <div class="typing-indicator">
                    <span></span><span></span><span></span>
                </div>
            </div>
        `;
        chatMessages.insertAdjacentHTML('beforeend', typingHTML);
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
        setTimeout(() => {
            // Scroll do container do chat
            chatMessages.scrollTo({
                top: chatMessages.scrollHeight,
                behavior: 'smooth'
            });
            // Caso a página inteira também role
            window.scrollTo({
                top: document.body.scrollHeight,
                behavior: 'smooth'
            });
        }, 100);
    }

    // Função que faz o fetch para a API Flask (app.py)
    async function processLLMMessage(userMessage) {
        return new Promise(async (resolve, reject) => {
            console.log("=== ENVIANDO PARA O BACK-END FLASK ===");
            try {
                const apiUrl = '/chat';

                const response = await fetch(apiUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        mensagem: userMessage,
                        nome: userData.nome,
                        estado: userData.estado,
                        formacao: userData.formacao,
                        ano: userData.ano,
                        hasCrea: userData.hasCrea
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

    // Função que faz o fetch para a extração do nome
    async function extractNameViaLLM(userMessage) {
        return new Promise(async (resolve, reject) => {
            try {
                const apiUrl = '/extract-name';
                const response = await fetch(apiUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ mensagem: userMessage })
                });

                if (!response.ok) {
                    throw new Error(`Erro HTTP: ${response.status}`);
                }

                const data = await response.json();
                if (data.erro) {
                    throw new Error(data.erro);
                }

                resolve(data.nome);
            } catch (error) {
                console.error("Erro na extração de nome:", error);
                reject(error.message);
            }
        });
    }
});
