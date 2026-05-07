# Usar a imagem oficial do Python, otimizada para tamanho e desempenho
FROM python:3.11-slim

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar os arquivos de requisitos e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação
COPY . .

# Expor a porta que o Cloud Run espera (8080)
EXPOSE 8080

# Comando para iniciar o servidor Gunicorn com a aplicação Flask
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "8", "--timeout", "0", "app:app"]
