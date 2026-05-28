// theme.js - Gerenciamento de Tema (Light/Dark Mode)
document.addEventListener('DOMContentLoaded', () => {
    // Busca o checkbox do switch
    const themeCheckbox = document.getElementById('themeCheckbox');
    const themeLabelText = document.getElementById('themeLabelText');
    
    // Checa a preferência salva ou a preferência do sistema
    const savedTheme = localStorage.getItem('creia-theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // O padrão é Dark Mode
    const isDarkMode = savedTheme === 'dark' || (!savedTheme && systemPrefersDark);
    
    // Inicializa a UI
    if (!isDarkMode) {
        document.documentElement.setAttribute('data-theme', 'light');
        if (themeCheckbox) themeCheckbox.checked = true; // Checked = Light Mode
        if (themeLabelText) themeLabelText.textContent = 'Light Mode';
    } else {
        document.documentElement.removeAttribute('data-theme');
        if (themeCheckbox) themeCheckbox.checked = false; // Unchecked = Dark Mode
        if (themeLabelText) themeLabelText.textContent = 'Dark Mode';
    }

    // Escuta mudanças no switch
    if (themeCheckbox) {
        themeCheckbox.addEventListener('change', (e) => {
            const isLight = e.target.checked;
            
            if (isLight) {
                document.documentElement.setAttribute('data-theme', 'light');
                localStorage.setItem('creia-theme', 'light');
                if (themeLabelText) themeLabelText.textContent = 'Light Mode';
            } else {
                document.documentElement.removeAttribute('data-theme');
                localStorage.setItem('creia-theme', 'dark');
                if (themeLabelText) themeLabelText.textContent = 'Dark Mode';
            }
        });
    }
});
