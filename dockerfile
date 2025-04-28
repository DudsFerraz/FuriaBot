# Usa imagem que já tem Python + Chrome
FROM ghcr.io/puppeteer/puppeteer:latest

# Instala Python
RUN apt-get update && apt-get install -y python3 python3-pip

# Define diretório de trabalho
WORKDIR /app

# Copia o projeto para dentro do container
COPY . .

# Instala dependências Python
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Porta padrão
ENV PORT=8080

# Expõe a porta
EXPOSE 8080

# Comando para iniciar o bot
CMD ["python3", "src/chatBot.py"]